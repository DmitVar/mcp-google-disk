"""upload_file tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import decode_content, upload_from_bytes, wrap_fail, wrap_ok


async def upload_file(
    name: str,
    content: str | bytes,
    parent_id: str | None = None,
    mime_type: str | None = None,
) -> dict[str, Any]:
    """Upload a file to Drive."""
    try:
        service = _helpers.get_service()
        data = decode_content(content)
        file = upload_from_bytes(service, name, data, parent_id=parent_id, mime_type=mime_type)
        return wrap_ok({"file_id": file.get("id"), "name": file.get("name"), "web_link": file.get("webLink")})
    except Exception as exc:
        return wrap_fail(exc, "upload_file failed")