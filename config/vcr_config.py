"""
VCR configuration for recording and replaying HTTP requests.
"""

import base64
import hashlib
import json
import logging
import os
from email.parser import BytesParser
from email.policy import default
from urllib.parse import parse_qsl, urlencode

import vcr
import vcr.stubs

VCR_MODE = os.getenv("VCR_MODE", "playback")
VCR_ENABLED = os.getenv("VCR_ENABLED", "false").lower() == "true"
VCR_CASSETTE_DIR = "vcr_cassettes"


_HEADERS_TO_REMOVE = [
    "Authorization",
    "X-API-Key",
    "Cookie",
    "Set-Cookie",
    "X-CSRF-Token",
]

_VCR_BOUNDARY = "vcr_cassette_boundary"
_PARTS_PREFIX = "vcr-multipart-parts:"

os.makedirs(VCR_CASSETTE_DIR, exist_ok=True)


_ORIGINAL_VCRHTTPRESPONSE_INIT = vcr.stubs.VCRHTTPResponse.__init__


def _remove_header_case_insensitive(headers: dict, name: str):
    for key in list(headers.keys()):
        if key.lower() == name.lower():
            del headers[key]


def _rebuild_multipart_body(parts: list, boundary: str) -> bytes:
    chunks = []

    for part in parts:
        chunks.append(f"--{boundary}".encode("ascii"))
        chunks.append(f"Content-Type: {part['content_type']}".encode("ascii"))

        for hk, hv in part["extra_headers"].items():
            chunks.append(f"{hk}: {hv}".encode("ascii"))

        chunks.append(b"")
        chunks.append(part["body"])

    chunks.append(f"--{boundary}--".encode("ascii"))
    return b"\r\n".join(chunks) + b"\r\n"


def _cassette_string_to_multipart_bytes(value) -> bytes:
    if isinstance(value, bytes):
        value = value.decode("utf-8")

    raw = json.loads(value[len(_PARTS_PREFIX) :])

    parts = []
    for item in raw:
        if item.get("encoding") == "base64":
            body_bytes = base64.b64decode(item["body"])
        else:
            body_bytes = item["body"].encode("utf-8")

        parts.append(
            {
                "content_type": item["content_type"],
                "extra_headers": item["extra_headers"],
                "body": body_bytes,
            }
        )

    return _rebuild_multipart_body(parts, _VCR_BOUNDARY)


def _patched_vcrhttpresponse_init(self, recorded_response):
    body = recorded_response.get("body", {})
    headers = recorded_response.get("headers", {})

    if isinstance(body, dict) and "string" in body:
        value = body["string"]

        if isinstance(value, str) and value.startswith(_PARTS_PREFIX):
            body["string"] = _cassette_string_to_multipart_bytes(value)
            _remove_header_case_insensitive(headers, "Content-Encoding")
            _remove_header_case_insensitive(headers, "Transfer-Encoding")

        elif isinstance(value, bytes) and value.startswith(_PARTS_PREFIX.encode("utf-8")):
            body["string"] = _cassette_string_to_multipart_bytes(value)
            _remove_header_case_insensitive(headers, "Content-Encoding")
            _remove_header_case_insensitive(headers, "Transfer-Encoding")

        elif isinstance(value, str):
            body["string"] = value.encode("utf-8")

    return _ORIGINAL_VCRHTTPRESPONSE_INIT(self, recorded_response)


if vcr.stubs.VCRHTTPResponse.__init__ is not _patched_vcrhttpresponse_init:
    vcr.stubs.VCRHTTPResponse.__init__ = _patched_vcrhttpresponse_init


def _filter_headers(headers):
    return {k: v for k, v in headers.items() if k not in _HEADERS_TO_REMOVE}


def _get_header(headers: dict, name: str):
    for k, v in headers.items():
        if k.lower() == name.lower():
            return k, (v[0] if isinstance(v, list) else v)
    return None, None


def _set_header(headers: dict, key: str, new_value: str):
    existing = headers.get(key)
    headers[key] = [new_value] if isinstance(existing, list) else new_value


def _normalise_request_body(body):
    if body is None:
        return b""
    if isinstance(body, bytes):
        return body
    if isinstance(body, str):
        return body.encode("utf-8")
    return str(body).encode("utf-8")


def _parse_form_body(body_bytes: bytes) -> dict[str, str]:
    text = body_bytes.decode("utf-8", errors="replace")
    return dict(parse_qsl(text, keep_blank_values=True))


def _normalise_json_string(value: str) -> str:
    try:
        return json.dumps(json.loads(value), sort_keys=True, separators=(",", ":"))
    except Exception:
        return value.strip()


def _body_matcher(r1, r2):
    body1 = _normalise_request_body(getattr(r1, "body", None))
    body2 = _normalise_request_body(getattr(r2, "body", None))

    uri1 = getattr(r1, "uri", "") or ""
    uri2 = getattr(r2, "uri", "") or ""

    if uri1.endswith("/LATEST/invoke"):
        return True

    if uri1 != uri2:
        return body1 == body2

    if uri1.endswith("/LATEST/eval"):
        form1 = _parse_form_body(body1)
        form2 = _parse_form_body(body2)

        if form1.keys() != form2.keys():
            return False

        for key in form1:
            v1 = form1[key]
            v2 = form2[key]

            if key == "vars":
                if _normalise_json_string(v1) != _normalise_json_string(v2):
                    return False
            else:
                if v1.strip() != v2.strip():
                    return False

        return True

    return body1 == body2


def _parts_to_cassette_string(parts: list) -> str:
    serialisable = []

    for part in parts:
        body_bytes = part["body"]
        if not isinstance(body_bytes, bytes):
            body_bytes = str(body_bytes).encode("utf-8")

        try:
            body_text = body_bytes.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            body_text = base64.b64encode(body_bytes).decode("ascii")
            encoding = "base64"

        serialisable.append(
            {
                "content_type": part["content_type"],
                "extra_headers": part["extra_headers"],
                "body": body_text,
                "encoding": encoding,
            }
        )

    return _PARTS_PREFIX + json.dumps(serialisable)


def _extract_all_parts_from_multipart(raw_body: str | bytes, content_type: str) -> list:
    if isinstance(raw_body, str):
        raw_body = raw_body.encode("utf-8")

    header_bytes = b"Content-Type: " + content_type.encode("ascii", errors="ignore") + b"\r\n\r\n"
    msg = BytesParser(policy=default).parsebytes(header_bytes + raw_body)

    parts = []
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue

        part_ct = part.get_content_type() or "application/octet-stream"
        payload = part.get_payload(decode=True) or b""

        if part_ct == "application/json" and payload:
            try:
                payload = json.dumps(json.loads(payload.decode("utf-8"))).encode("utf-8")
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                logging.debug("Failed to parse json part: %s", exc)

        extra = {k: v for k, v in part.items() if k.lower() != "content-type"}
        parts.append(
            {
                "content_type": part_ct,
                "extra_headers": extra,
                "body": payload,
            }
        )

    return parts


def _before_record_request(request):
    request.headers = _filter_headers(request.headers)

    if isinstance(getattr(request, "body", None), str):
        request.body = request.body.encode("utf-8")

    return request


def _before_record_response(response):
    response["headers"] = _filter_headers(response["headers"])

    ct_key, content_type = _get_header(response["headers"], "content-type")
    if not content_type or "multipart" not in content_type.lower():
        return response

    raw_body = response["body"].get("string", b"")
    transformed_body = raw_body

    ce_key, content_encoding = _get_header(response["headers"], "content-encoding")
    if content_encoding and isinstance(raw_body, bytes):
        import gzip
        import zlib

        try:
            if "gzip" in content_encoding.lower():
                transformed_body = gzip.decompress(raw_body)
            elif "deflate" in content_encoding.lower():
                transformed_body = zlib.decompress(raw_body)
        except Exception:
            transformed_body = raw_body

    try:
        parts = _extract_all_parts_from_multipart(transformed_body, content_type)
    except Exception:
        return response

    if not parts:
        return response

    response["body"]["string"] = _parts_to_cassette_string(parts)

    subtype = content_type.split(";")[0].strip()
    _set_header(response["headers"], ct_key, f"{subtype}; boundary={_VCR_BOUNDARY}")

    if ce_key:
        del response["headers"][ce_key]
    _remove_header_case_insensitive(response["headers"], "Transfer-Encoding")

    return response


def get_vcr_instance():
    record_mode = "all" if (VCR_ENABLED and VCR_MODE == "record") else "none"

    my_vcr = vcr.VCR(
        cassette_library_dir=VCR_CASSETTE_DIR,
        record_mode=record_mode,
        match_on=["method", "scheme", "host", "port", "path", "query", "body"],
        before_record_request=_before_record_request,
        before_record_response=_before_record_response,
        filter_headers=["User-Agent", "Accept-Encoding", "Connection", "Content-Length"],
        decode_compressed_response=False,
    )

    # my_vcr.register_matcher("body", _body_matcher)
    return my_vcr


def cassette_name_for_request(method: str, path: str, query_string: str = "") -> str:
    slug = path.strip("/").replace("/", "_")
    base = f"{slug}_{method.lower()}"

    if not query_string:
        return base

    sorted_params = urlencode(sorted(parse_qsl(query_string, keep_blank_values=True)))
    param_hash = hashlib.sha256(sorted_params.encode()).hexdigest()[:8]

    return f"{base}_{param_hash}"


class VCRContext:
    def __init__(self, cassette_name: str):
        self.cassette_name = cassette_name
        self.vcr = get_vcr_instance()
        self.cassette = None

    @classmethod
    def for_request(cls, method: str, path: str, query_string: str = "") -> "VCRContext":
        return cls(cassette_name_for_request(method, path, query_string))

    def __enter__(self):
        self.cassette = self.vcr.use_cassette(f"{self.cassette_name}.yaml", allow_playback_repeats=True)
        return self.cassette.__enter__()

    def __exit__(self, *args):
        return self.cassette.__exit__(*args)
