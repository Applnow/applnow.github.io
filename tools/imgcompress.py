#!/usr/bin/env python3
"""图片压缩与规范化命名的共享实现。

被两个入口调用：
  tools/normalize-images.py   整理仓库内已有图片
  tools/upload-images.py      处理文章里待上传的图片

命名规则（站点图片与图床对象名共用同一条规则）：

    <语义名>-<内容哈希前 8 位>.webp

语义名由文件原有的名字归一而来（中文或带空格的清掉），例如
`Patchouli Knowledge.jpg` -> `patchouli-knowledge-5857f110.webp`。
哈希取自**原始文件内容**，因此同一张图重复处理会得到同一个名字，
不同内容的图永远不会撞名——不需要额外查重，也不需要人工避让。
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass

# 已确定相关性的扩展名；原图备份与站点成品都走这套规则
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff", ".webp"}

WEBP_QUALITY = 82
WEBP_METHOD = 6


@dataclass
class ProcessResult:
    src: str
    dest: str
    sha1: str
    width: int
    height: int
    src_bytes: int
    dest_bytes: int
    method: str
    skipped: bool = False

    @property
    def ratio(self) -> float:
        if not self.src_bytes:
            return 0.0
        return 100.0 - self.dest_bytes * 100.0 / self.src_bytes


def content_sha1(path: str) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(stem: str) -> str:
    """把任意文件名主体归一成 URL 安全的小写连字符形式。"""
    s = stem.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "image"


# 已规范化文件名末尾的 <8 位十六进制哈希>。反复处理时必须先剥掉它，
# 否则每次都会把新哈希再追加一次，名字无限变长、也永不收敛。
_HASH_SUFFIX = re.compile(r"-[0-9a-f]{8}$")


def base_slug(name: str) -> str:
    """从文件名（可含目录）取出「语义名」，剥掉已有的哈希后缀与扩展名。"""
    stem = os.path.splitext(os.path.basename(name))[0]
    return _HASH_SUFFIX.sub("", slugify(stem))


def normalized_name(stem: str, sha1: str, ext: str = ".webp") -> str:
    return f"{base_slug(stem)}-{sha1[:8]}{ext}"


def _pillow():
    try:
        from PIL import Image, ImageFile  # noqa: F401
    except ImportError as exc:  # pragma: no cover - 环境问题
        raise SystemExit(
            "缺少 Pillow。本仓库用 tools/ 下的虚拟环境，先执行：\n"
            "  python3 -m venv tools/.venv && tools/.venv/bin/pip install Pillow\n"
            f"（原始错误：{exc}）"
        )
    from PIL import Image, ImageFile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    return Image


def _has_real_alpha(im) -> bool:
    """只有真的含半透明像素时才保留 alpha，避免无谓的 RGBA 体积。"""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        a = im.convert("RGBA").getchannel("A")
        w, h = im.size
        return a.getbbox() != (0, 0, w, h)
    return False


def process_image(src: str, dest: str | None = None, quality: int = WEBP_QUALITY) -> ProcessResult:
    """把 src 压成 WebP 写到 dest，返回处理结果。

    若源文件本身已是 WebP，直接沿用原始字节：重新编码只会二次损失画质，
    有时反而更大（实测 reimu.jpg 就是这种扩展名骗人的情况）。
    """
    Image = _pillow()
    raw = open(src, "rb").read()
    sha = hashlib.sha1(raw).hexdigest()

    im = Image.open(src)
    fmt = (im.format or "").upper()
    width, height = im.size
    if dest is None:
        stem = os.path.splitext(os.path.basename(src))[0]
        dest = os.path.join(os.path.dirname(src), normalized_name(stem, sha))

    if fmt == "WEBP":
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
        with open(dest, "wb") as f:
            f.write(raw)
        return ProcessResult(src, dest, sha, width, height, len(raw), len(raw),
                             "沿用原始 WebP 字节", skipped=True)

    if _has_real_alpha(im):
        out = im.convert("RGBA")
    else:
        out = im.convert("RGB")
    os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)
    out.save(dest, "WEBP", quality=quality, method=WEBP_METHOD)
    return ProcessResult(src, dest, sha, width, height, len(raw), os.path.getsize(dest),
                         f"WebP q{quality}")


def human(n: int) -> str:
    for unit in ("B", "K", "M"):
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024.0
    return f"{n:.0f}G"
