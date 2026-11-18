#!/usr/bin/env python3
"""Cloudflare R2（S3 兼容 API）上传客户端。

只依赖标准库：R2 与所有 S3 兼容服务都用 AWS Signature V4，而 V4 不过是
几轮 HMAC-SHA256，没必要为此拉进 boto3 那套依赖。

区域固定写 "auto"——R2 不接受真实区域名。
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import hmac
import mimetypes
import urllib.error
import urllib.parse
import urllib.request

ALGORITHM = "AWS4-HMAC-SHA256"
SERVICE = "s3"
REGION = "auto"


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hmac(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _signing_key(secret: str, date: str) -> bytes:
    k = _hmac(("AWS4" + secret).encode("utf-8"), date)
    k = _hmac(k, REGION)
    k = _hmac(k, SERVICE)
    return _hmac(k, "aws4_request")


def sign_put(url: str, access_key: str, secret_key: str, payload: bytes,
             now: _dt.datetime | None = None,
             extra_headers: dict[str, str] | None = None) -> dict[str, str]:
    """为一次 PUT 生成完整的请求头（含 Authorization）。"""
    now = now or _dt.datetime.now(_dt.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date = now.strftime("%Y%m%d")

    parsed = urllib.parse.urlsplit(url)
    # 路径中的每一段都要单独百分号编码，但 '/' 本身保留
    canonical_uri = urllib.parse.quote(parsed.path or "/", safe="/~")
    canonical_query = parsed.query  # 我们不用查询参数，保持原样

    headers = {
        "host": parsed.netloc,
        "x-amz-content-sha256": _sha256_hex(payload),
        "x-amz-date": amz_date,
    }
    for k, v in (extra_headers or {}).items():
        headers[k.lower()] = v
    if "content-type" not in headers:
        headers["content-type"] = "application/octet-stream"

    signed_names = sorted(headers)
    canonical_headers = "".join(f"{k}:{headers[k].strip()}\n" for k in signed_names)
    signed_headers = ";".join(signed_names)

    canonical_request = "\n".join([
        "PUT", canonical_uri, canonical_query,
        canonical_headers, signed_headers, headers["x-amz-content-sha256"],
    ])
    scope = f"{date}/{REGION}/{SERVICE}/aws4_request"
    string_to_sign = "\n".join([
        ALGORITHM, amz_date, scope, _sha256_hex(canonical_request.encode("utf-8")),
    ])
    signature = hmac.new(_signing_key(secret_key, date),
                         string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    headers["authorization"] = (
        f"{ALGORITHM} Credential={access_key}/{scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return headers


def put_object(endpoint: str, bucket: str, key: str, data: bytes,
               access_key: str, secret_key: str, content_type: str | None = None,
               timeout: int = 60) -> str:
    """上传一个对象，返回它的 URL。失败抛 RuntimeError。"""
    endpoint = endpoint.rstrip("/")
    url = f"{endpoint}/{bucket}/{urllib.parse.quote(key, safe='/~')}"
    extra = {}
    ctype = content_type or mimetypes.guess_type(key)[0]
    if ctype:
        extra["content-type"] = ctype
    headers = sign_put(url, access_key, secret_key, data, extra_headers=extra)

    request = urllib.request.Request(url, data=data, method="PUT")
    for k, v in headers.items():
        # urllib 会自动补 Host，重复设置会冲突
        if k.lower() == "host":
            continue
        request.add_header(k, v)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"上传失败：HTTP {resp.status} {url}")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"上传失败：HTTP {exc.code} {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"无法连接 {endpoint}：{exc.reason}") from exc
    return url
