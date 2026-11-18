#!/usr/bin/env python3
"""把 Noto Serif SC 子集化并本地化到站点，替代 Google Fonts 的远程加载。

背景与动机
----------
_includes/head.html 原来直接引 Google Fonts 的 CSS2 接口。实测那份 CSS 有 330 KB、
对应 3 个字重 × 101 个 unicode-range 分片（单字重覆盖约 16000 码位），
而全站自有 CSS + JS 合计只有约 35 KB —— 字体才是首屏的真正阻塞项。
本站正文实际只用到约 2500 个字符，按站点实际用字做子集，体积可降一个数量级。

为什么不沿用 Google 的分片
--------------------------
曾按 Google 的 unicode-range 分片粒度做子集（258 个分片，去重后 86 个文件）。
实测每页仍要下载 740–957 KB、发出 13–29 个请求：Google 的分片是按「中文常用字」
设计的，每片覆盖 102–181 个码位、均 13–43 KB，而本站每片平均只用到约 10 个字，
整片下载的冗余极大。改为「一份包含全站用字的单一文件」后，每页固定 859,560 字节、
只发 1 个请求，fonts.css 也从 109.7 KB 降到约 0.6 KB。

另有两个实测结论决定了现在的形状：
- Google Fonts 对 Noto Serif SC 的 400 / 600 / 700 返回的是逐字节相同的文件
  （sha256 三个列表完全一致），即那「三个字重」从来只有一份 ExtraLight 字形数据，
  粗体由浏览器合成。所以本地版本也只需一份字形数据。
- 字体源取 noto-cjk 官方的可变字体 NotoSerifSC-VF.otf（22.6 MB），子集后仍是
  可变字体（wght 轴 200–900，默认 200），一份文件即可覆盖 CSS 里的 400/600/700。

做法
----
1. 扫描仓库里所有会被输出的文本文件，收集站点实际用字。
2. 下载 noto-cjk 的可变字体到 _fonts/ 缓存（22.6 MB，只下一次）。
3. 用 pyftsubset 按站点用字裁出单一 woff2 -> assets/fonts/。
4. 生成 assets/css/fonts.css：三条 @font-face（400 / 600 / 700）指向同一文件。

用法
----
    tools/.venv/bin/python tools/fonts.py            # 增量：已是最新则跳过
    tools/.venv/bin/python tools/fonts.py --force    # 强制重建（含重新下载源字体）

新增文章若用到清单外的字，会回落到 hyde.css 字体链里的系统字体（SimSun/宋体等），
不会出现方框；要把它纳入子集，重跑本脚本即可。
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "_fonts"          # 中间产物：源字体、字符清单（.gitignore 已忽略）
OUT_FONT_DIR = ROOT / "assets" / "fonts"
FONTS_CSS = ROOT / "assets" / "css" / "fonts.css"
SUBSET_PY = ROOT / "tools" / ".venv" / "bin" / "pyftsubset"

FAMILY = "Noto Serif SC"
WEIGHTS = ["400", "600", "700"]          # 与 hyde.css 里用到的字重保持一致
# noto-cjk 官方的简体中文可变字体（Serif/Variable/OTF/Subset/，含完整 wght 轴）
SOURCE_URL = (
    "https://github.com/notofonts/noto-cjk/raw/main/"
    "Serif/Variable/OTF/Subset/NotoSerifSC-VF.otf"
)
SOURCE_NAME = "NotoSerifSC-VF.otf"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
# 扫描范围：会被 Jekyll 输出或参与正文渲染的文本文件
SCAN_GLOBS = ["*.md", "*.html", "*.yml", "*.xml", "*.js", "*.css", "*.markdown"]
SCAN_EXCLUDE_DIRS = {"_site", "_fonts", ".git", "vendor", ".venv", "__pycache__", "_img", "tools"}
# 额外补充：站点今后可能出现、但当前文件里没有的常用标点与符号
EXTRA_CHARS = "　、。〈〉《》「」『』【】〔〕・ーー—–…‘’“”·×÷≈≠≤≥°±§¶†‡•‰′″€£¥$¢©®™←→↑↓⇄⇒"


def scan_chars() -> set[str]:
    """扫描仓库文本，返回站点实际用到的字符集合。"""
    files: list[Path] = []
    for pattern in SCAN_GLOBS:
        for p in glob.glob(str(ROOT / pattern)) + glob.glob(str(ROOT / "*" / pattern)):
            path = Path(p)
            if any(part in SCAN_EXCLUDE_DIRS for part in path.relative_to(ROOT).parts):
                continue
            files.append(path)
    chars: set[str] = set(EXTRA_CHARS)
    for path in sorted(set(files)):
        try:
            chars |= set(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, OSError):
            continue
    # 丢掉控制字符
    return {c for c in chars if c.isprintable() or c == " "}


def cmap_codepoints(font_path: Path) -> set[int]:
    """读字体真实的 cmap，返回它包含字形的码位集合。"""
    from fontTools.ttLib import TTFont
    with TTFont(font_path, lazy=True) as ft:
        return set(ft.getBestCmap().keys())


def download(url: str, cache_file: Path, force: bool = False) -> Path:
    """带本地缓存的下载；先写临时文件再改名，避免中断留下半个文件。"""
    if cache_file.exists() and cache_file.stat().st_size > 0 and not force:
        return cache_file
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = cache_file.with_suffix(cache_file.suffix + ".part")
    print(f"      下载 {url}")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=600) as resp, tmp.open("wb") as fh:
        shutil.copyfileobj(resp, fh, length=1 << 20)
    tmp.replace(cache_file)
    return cache_file


def run_subset(src: Path, dst: Path, text_file: Path) -> bool:
    """用 pyftsubset 裁出子集，输出 woff2。"""
    if not SUBSET_PY.exists():
        raise FileNotFoundError(
            f"缺少 {SUBSET_PY}\n"
            "先执行： python3 -m venv tools/.venv && tools/.venv/bin/pip install fonttools brotli"
        )
    cmd = [
        str(SUBSET_PY), str(src),
        f"--text-file={text_file}",
        "--flavor=woff2",
        f"--output-file={dst}",
        "--layout-features=*",
        "--no-hinting",
        "--desubroutinize",
        "--name-IDs=*",
        "--drop-tables+=DSIG",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"      pyftsubset 失败：{proc.stderr.strip()[:400]}")
        return False
    return dst.exists() and dst.stat().st_size > 0


def drop_old_outputs(keep: Path) -> int:
    """清掉上一次运行留下的字体文件（分片方案会留下几十个）。"""
    removed = 0
    for old in OUT_FONT_DIR.glob("*.woff2"):
        if old != keep:
            old.unlink()
            removed += 1
    return removed


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="忽略缓存，强制重建（含重新下载源字体）")
    args = ap.parse_args()

    if not SUBSET_PY.exists():
        print(f"缺少 {SUBSET_PY}\n先执行： python3 -m venv tools/.venv && tools/.venv/bin/pip install fonttools brotli")
        return 1

    CACHE.mkdir(exist_ok=True)
    OUT_FONT_DIR.mkdir(parents=True, exist_ok=True)
    FONTS_CSS.parent.mkdir(parents=True, exist_ok=True)

    # 1. 站点用字
    chars = scan_chars()
    text_file = CACHE / "chars.txt"
    text_file.write_text("".join(sorted(chars)), encoding="utf-8")
    chars_hash = hashlib.sha256("".join(sorted(chars)).encode()).hexdigest()[:12]
    print(f"[1/4] 站点用字 {len(chars)} 个（指纹 {chars_hash}）")

    # 2. 源字体（可变字体，含完整 wght 轴）
    src = download(SOURCE_URL, CACHE / SOURCE_NAME, args.force)
    print(f"[2/4] 源字体 {src.name}：{src.stat().st_size / 1024 / 1024:.1f} MB")

    # 3. 子集化
    out_name = f"noto-serif-sc-{chars_hash}.woff2"
    out_path = OUT_FONT_DIR / out_name
    if args.force or not out_path.exists():
        if not run_subset(src, out_path, text_file):
            return 1
    size = out_path.stat().st_size
    print(f"[3/4] 子集 -> assets/fonts/{out_name}：{size:,} 字节（{size / 1024:.1f} KB），1 个文件")

    # 覆盖度自检：用子集字体真实的 cmap 判断站内用字是否都有字形
    real_cmap = cmap_codepoints(out_path)
    missing = sorted(c for c in chars if ord(c) not in real_cmap)
    if missing:
        preview = "".join(missing[:40])
        print(f"      提示：{len(missing)} 个字符在字体中无字形，将回落到系统字体：{preview}"
              f"{' …' if len(missing) > 40 else ''}")
    else:
        print("      自检：站内用字全部有对应字形")

    # 4. 输出 fonts.css
    #
    # 三条 @font-face 指向同一个文件，不是冗余：Google Fonts 对 400/600/700 返回的
    # 本来就是同一份数据，本地子集也是可变字体（wght 200-900），浏览器只下载一次。
    # 不写成 font-weight: 400 600 700 的范围形式，是为了兼容老浏览器的解析。
    lines = [
        "---",
        "# 空 front matter：让 Jekyll 处理本文件里的 {{ }} 与 relative_url",
        "---",
        "/* 本地字体，由 tools/fonts.py 自动生成，请勿手工编辑。",
        f" * 来源：noto-cjk 的 {FAMILY} 可变字体，按站内 {len(chars)} 个用字子集化。",
        f" * 单文件 {size:,} 字节（{size / 1024:.1f} KB），覆盖 400/600/700 全字重；",
        " * 与 hyde.css 的 'Noto Serif SC' 同名，字体链其余部分作为缺字回退。",
        " * 由 _includes/head.html 引入，须排在 hyde.css 之前。",
        " */",
    ]
    for weight in WEIGHTS:
        lines += [
            "@font-face {",
            f"  font-family: '{FAMILY}';",
            "  font-style: normal;",
            f"  font-weight: {weight};",
            "  font-display: swap;",
            f"  src: url('{{{{ '/assets/fonts/{out_name}' | relative_url }}}}') format('woff2');",
            "}",
        ]
    lines.append("")
    FONTS_CSS.write_text("\n".join(lines), encoding="utf-8")

    removed = drop_old_outputs(out_path)
    print(f"[4/4] assets/css/fonts.css：{len(WEIGHTS)} 条 @font-face -> 1 个文件"
          f"{f'（清理旧文件 {removed} 个）' if removed else ''}")

    manifest = {
        "chars": len(chars),
        "chars_hash": chars_hash,
        "file": out_name,
        "bytes": size,
        "weights": WEIGHTS,
        "missing_chars": "".join(missing),
    }
    (CACHE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n完成：assets/css/fonts.css 与 assets/fonts/{out_name} 已更新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
