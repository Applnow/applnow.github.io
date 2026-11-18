#!/usr/bin/env python3
"""把正文里引用的本地图片上传到 Cloudflare R2，并把链接回填成外链。

设计上的三条硬约束：
  1. **不动方括号里的说明文字**。`![说明](url)` 的说明会进 img.alt，
     而灯箱下方的图注正是从 alt 取的——所以只替换 URL 部分，一个字都不碰。
  2. **跑第二遍不会重复上传**。账本记在 _img/uploaded.json，键是文件内容的
    哈希，因此改名、换目录、重复引用同一张图都不会二次上传。
  3. **默认只预报**。加 --apply 才真正上传并改写文件。

用法：
    tools/.venv/bin/python tools/upload-images.py                    # 预报
    tools/.venv/bin/python tools/upload-images.py --apply            # 执行
    tools/.venv/bin/python tools/upload-images.py --apply --files _posts/xxx.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgcompress import IMAGE_EXTS, base_slug, process_image  # noqa: E402
import r2  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT, "_img", "r2.json")
LEDGER_PATH = os.path.join(ROOT, "_img", "uploaded.json")
ORIGINALS = os.path.join(ROOT, "_img", "originals")
INCOMING = os.path.join(ROOT, "_img", "incoming")

SCAN_EXTS = (".md", ".markdown", ".html")

def _skip_url(text: str, i: int) -> int:
    """跳过一段可能带 <> 包裹的 URL，返回右括号位置（找不到返回 -1）。"""
    n = len(text)
    if i < n and text[i] == "<":
        end = text.find(">", i)
        if end == -1:
            return -1
        i = end + 1
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == "(":      # 路径里的括号允许成对出现
            depth = 1
            i += 1
            while i < n and depth:
                if text[i] == "(":
                    depth += 1
                elif text[i] == ")":
                    depth -= 1
                i += 1
            continue
        if c == ")":
            return i
        i += 1
    return -1


def iter_md_images(text: str):
    """逐个产出 (URL 起始下标, URL 结束下标)。方括号计数，所以 alt 里嵌套
    方括号（如 `![图[1]说明](...)`）也不会漏掉这张图。"""
    n = len(text)
    i = 0
    while True:
        i = text.find("![", i)
        if i == -1:
            return
        j = i + 2
        depth = 0
        close = -1
        while j < n:                      # 找到与 `![` 配对的 `]`
            c = text[j]
            if c == "\\":
                j += 2
                continue
            if c == "[":
                depth += 1
            elif c == "]":
                if depth == 0:
                    close = j
                    break
                depth -= 1
            j += 1
        if close == -1 or close + 1 >= n or text[close + 1] != "(":
            i += 2
            continue
        end = _skip_url(text, close + 2)
        if end == -1:
            i += 2
            continue
        yield close + 2, end
        i = end + 1


# HTML img 的 src，单双引号都收
HTML_IMG = re.compile(r"(<img\b[^>]*?\bsrc=)([\"'])([^\"']+)(\2)", re.IGNORECASE)
# JS 里的图片清单：{ src: '/assets/images/foo.webp', caption: '...' }
JS_SRC = re.compile(r"\bsrc\s*:\s*([\"'])([^\"']+)(\1)")
# 默认全仓库扫描时额外带上这些文件（图片清单写在 JS 里，不在正文里）
EXTRA_TARGETS = ("assets/album.js",)


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        raise SystemExit(
            f"缺少 R2 配置：{CONFIG_PATH}\n"
            "先照 README 的「图片托管」一节填好 endpoint / bucket / 密钥与公开域名。"
        )
    cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
    missing = [k for k in ("endpoint", "bucket", "access_key_id", "secret_access_key", "public_base")
               if not cfg.get(k)]
    if missing:
        raise SystemExit(f"R2 配置缺少字段：{', '.join(missing)}")
    return cfg


def load_json(path: str, default):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return default


def save_json(path: str, data) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def is_local_ref(ref: str) -> bool:
    if ref.startswith(("http://", "https://", "//", "data:", "mailto:", "#")):
        return False
    return os.path.splitext(ref.split("?")[0].split("#")[0])[1].lower() in IMAGE_EXTS


def resolve(ref: str, doc_path: str) -> str | None:
    """把正文里的引用解析成磁盘路径：先按站点根，再按文章所在目录。"""
    clean = ref.lstrip("/")
    for cand in (os.path.join(ROOT, clean),
                 os.path.join(os.path.dirname(doc_path), clean)):
        if os.path.isfile(cand):
            return os.path.normpath(cand)
    return None


def remote_url(cfg: dict, filename: str) -> str:
    base = cfg["public_base"].rstrip("/")
    prefix = cfg.get("prefix", "").strip("/")
    return f"{base}/{prefix + '/' if prefix else ''}{filename}"


def iter_js_images(text: str):
    """收集 JS 里形如 src: '/assets/images/foo.webp' 的本地图片引用，返回 (起, 止) 区间。

    相册的图片清单写在 assets/album.js 的数组里，Markdown/HTML 那两条规则扫不到它。
    """
    seen: set[str] = set()
    for m in JS_SRC.finditer(text):
        # group(1) 是引号，group(2) 才是路径
        ref = m.group(2)
        if ref in seen or not is_local_ref(ref):
            continue
        seen.add(ref)
        yield m.start(2), m.end(2)


def collect(doc_path: str) -> list[tuple[str, str]]:
    """返回 [(原始引用, 解析后的磁盘路径)]，按出现顺序去重。"""
    text = open(doc_path, encoding="utf-8").read()
    refs = [text[s:e] for s, e in iter_md_images(text)]
    refs += [m.group(3) for m in HTML_IMG.finditer(text)]
    if doc_path.endswith(".js"):
        refs += [text[s:e] for s, e in iter_js_images(text)]
    found, seen = [], set()
    for ref in refs:
        if not is_local_ref(ref):
            continue
        path = resolve(ref, doc_path)
        if path is None:
            print(f"  ⚠ {os.path.relpath(doc_path, ROOT)}：找不到 {ref}")
            continue
        if (ref, path) not in seen:
            seen.add((ref, path))
            found.append((ref, path))
    return found


# 默认扫描范围：站点页面 + 文章。README/AGENT 是给人和 agent 看的文档，
# 里面的示例路径不是真图片，扫进来只会刷无谓的警告。
SKIP_DOCS = {"README.md", "AGENT.md"}


def default_targets() -> list[str]:
    targets = []
    for name in sorted(os.listdir(ROOT)):
        if name in SKIP_DOCS:
            continue
        if os.path.isfile(os.path.join(ROOT, name)) and name.endswith(SCAN_EXTS):
            targets.append(os.path.join(ROOT, name))
    posts = os.path.join(ROOT, "_posts")
    if os.path.isdir(posts):
        targets += [os.path.join(posts, f) for f in sorted(os.listdir(posts))
                    if f.endswith(SCAN_EXTS)]
    for rel in EXTRA_TARGETS:
        path = os.path.join(ROOT, rel)
        if os.path.isfile(path):
            targets.append(path)
    return targets


def backup(path: str) -> None:
    try:
        rel = os.path.relpath(path, ROOT)
    except ValueError:
        return
    dest = os.path.join(ORIGINALS, rel)
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(path, dest)


def main() -> int:
    ap = argparse.ArgumentParser(description="上传正文图片到 R2 并回填链接")
    ap.add_argument("--apply", action="store_true", help="真正上传并改写文件（默认仅预报）")
    ap.add_argument("--files", nargs="*", help="只处理这些文件（默认全仓库扫描）")
    args = ap.parse_args()

    docs = args.files or default_targets()
    docs = [d if os.path.isabs(d) else os.path.join(ROOT, d) for d in docs]

    cfg = load_config() if args.apply else None
    ledger = load_json(LEDGER_PATH, {})
    uploaded_log = []

    total_before = total_after = 0
    plan = []
    for doc in docs:
        hits = collect(doc)
        if hits:
            plan.append((doc, hits))

    if not plan:
        print("没有发现需要上传的本地图片引用。")
        return 0

    for doc, hits in plan:
        rel_doc = os.path.relpath(doc, ROOT)
        print(f"\n{rel_doc}")
        for ref, path in hits:
            sha = hashlib.sha1(open(path, "rb").read()).hexdigest()
            total_before += os.path.getsize(path)
            if sha in ledger:
                url = ledger[sha]["url"]
                print(f"  {ref}")
                print(f"    已上传过，跳过（{ledger[sha]['name']}）")
            else:
                name = f"{base_slug(path)}-{sha[:8]}.webp"
                url = remote_url(cfg, name) if cfg else f"<{cfg or 'R2'}/{name}>"
                print(f"  {ref}")
                print(f"    -> {name}")
            if not args.apply:
                total_after += os.path.getsize(path)
                continue

            # 处理：压成 WebP + 规范命名，落到 _img/incoming/ 暂存
            backup(path)
            os.makedirs(INCOMING, exist_ok=True)
            staged = os.path.join(INCOMING, os.path.basename(url))
            res = process_image(path, staged)
            total_after += res.dest_bytes
            payload = open(res.dest, "rb").read()
            r2.put_object(cfg["endpoint"], cfg["bucket"], _key(cfg, os.path.basename(url)),
                          payload, cfg["access_key_id"], cfg["secret_access_key"],
                          content_type="image/webp")
            ledger[sha] = {"name": os.path.basename(url), "url": url,
                           "bytes": len(payload), "source": rel_doc}
            save_json(LEDGER_PATH, ledger)
            uploaded_log.append((rel_doc, ref, url))
            print(f"    已上传 {len(payload)/1024:.0f}K  [{res.method}]")

    if args.apply:
        # 回填：整文件做纯文本替换，只换 URL，方括号里的说明文字一个字都不碰
        replace_map = {}
        for doc, hits in plan:
            for ref, path in hits:
                sha = hashlib.sha1(open(path, "rb").read()).hexdigest()
                if sha in ledger:
                    # 用完整引用（含开头的 /）作键，否则替换后会残留一个斜杠
                    replace_map[ref] = ledger[sha]["url"]
        changed = []
        for doc, hits in plan:
            text = open(doc, encoding="utf-8").read()
            before = text
            for old, new in sorted(replace_map.items(), key=lambda kv: -len(kv[0])):
                if old in text:
                    text = text.replace(old, new)
            if text != before:
                open(doc, "w", encoding="utf-8").write(text)
                changed.append(os.path.relpath(doc, ROOT))
        print(f"\n共上传 {len(uploaded_log)} 张，账本记在 _img/uploaded.json")
        print(f"体积 {total_before/1024/1024:.2f}M -> 上传 {total_after/1024/1024:.2f}M")
        print(f"已回填 {len(changed)} 个文件：{', '.join(changed) if changed else '（无）'}")
    else:
        print("\n（预报模式，未上传也未改动文件。加 --apply 执行）")
    return 0


def _key(cfg: dict, name: str) -> str:
    prefix = cfg.get("prefix", "").strip("/")
    return f"{prefix}/{name}" if prefix else name


if __name__ == "__main__":
    raise SystemExit(main())
