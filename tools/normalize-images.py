#!/usr/bin/env python3
"""把仓库内的图片统一成「WebP + 内容寻址命名」。

默认只做预报（dry-run），加 --write 才真正改动磁盘。改动前每个被覆盖的
原文件都会备份到 _img/originals/<原相对目录>/，因此这一步是可逆的。

用法：
    tools/.venv/bin/python tools/normalize-images.py            # 看你有哪些图需要处理
    tools/.venv/bin/python tools/normalize-images.py --write    # 真正执行
    tools/.venv/bin/python tools/normalize-images.py --write --dirs images
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from imgcompress import IMAGE_EXTS, content_sha1, normalized_name, process_image  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_ROOT = os.path.join(ROOT, "_img", "originals")
DEFAULT_DIRS = ("assets/images", "images")


def iter_images(rel_dir: str):
    base = os.path.join(ROOT, rel_dir)
    if not os.path.isdir(base):
        return
    for name in sorted(os.listdir(base)):
        if name.endswith(":Zone.Identifier"):
            continue
        path = os.path.join(base, name)
        if os.path.isfile(path) and os.path.splitext(name)[1].lower() in IMAGE_EXTS:
            yield rel_dir, name, path


def main() -> int:
    ap = argparse.ArgumentParser(description="规范化仓库内图片（WebP + 内容命名）")
    ap.add_argument("--write", action="store_true", help="真正写入改动（默认仅预报）")
    ap.add_argument("--dirs", nargs="+", default=list(DEFAULT_DIRS),
                    help=f"要处理的目录，默认 {' '.join(DEFAULT_DIRS)}")
    args = ap.parse_args()

    todo, done = [], []
    for rel_dir in args.dirs:
        for rel_dir_, name, path in iter_images(rel_dir):
            stem, ext = os.path.splitext(name)
            sha = content_sha1(path)
            target_name = normalized_name(stem, sha)
            if name == target_name and ext.lower() == ".webp":
                done.append((rel_dir_, name))
            else:
                todo.append((rel_dir_, name, path, target_name, sha))

    if not todo:
        print("所有图片都已符合规范，无需处理。")
        return 0

    print(f"发现 {len(todo)} 张需要规范化的图片：\n")
    total_before = total_after = 0
    for rel_dir, name, path, target_name, sha in todo:
        before = os.path.getsize(path)
        total_before += before
        if args.write:
            # 先备份原文件（保留原始相对路径），再落新文件
            backup = os.path.join(BACKUP_ROOT, rel_dir, name)
            os.makedirs(os.path.dirname(backup), exist_ok=True)
            if not os.path.exists(backup):
                shutil.copy2(path, backup)
            dest = os.path.join(ROOT, rel_dir, target_name)
            res = process_image(path, dest)
            if os.path.abspath(path) != os.path.abspath(dest):
                os.remove(path)
            total_after += res.dest_bytes
            print(f"  {rel_dir}/{name}")
            print(f"    -> {target_name}   {before/1024:.0f}K -> {res.dest_bytes/1024:.0f}K "
                  f"(-{res.ratio:.0f}%)  {res.width}x{res.height}  [{res.method}]")
        else:
            total_after += before
            print(f"  {rel_dir}/{name}  ->  {target_name}   （预报，未改动）")

    if args.write:
        print(f"\n合计 {total_before/1024/1024:.2f}M -> {total_after/1024/1024:.2f}M "
              f"(-{100-total_after*100/total_before:.0f}%)")
        print(f"原图已备份到 _img/originals/")
        print("\n注意：文件名变了，引用它们的地方需要同步改写——")
        print("      grep -rn \"旧文件名\" . 找出所有引用点后再改。")
    else:
        print("\n（预报模式，未改动任何文件。加 --write 执行）")
        print("注意：文件名会变，执行后必须同步改写所有引用点。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
