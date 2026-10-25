"""download_file tool."""

from __future__ import annotations

import base64
from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def download_file(file_id: str, mime_type: str | None = None, output_path: str | None = None) -> dict[str, Any]:
    """Download a Drive file (optionally converting Google-native formats)."""
    try:
        service = _helpers.get_service()
        meta = service.files().get(fileId=file_id, fields="id,name,mimeType").execute()
        content = _helpers.download_to_bytes(service, file_id, mime_type)
        if output_path:
            with open(output_path, "wb") as fh:
                fh.write(content)
            return wrap_ok({"file_id": meta.get("id"), "name": meta.get("name"), "path": output_path})
        return wrap_ok(
            {
                "file_id": meta.get("id"),
                "name": meta.get("name"),
                "mime_type": meta.get("mimeType"),
                "content_base64": base64.b64encode(content).decode("ascii"),
            }
        )
    except Exception as exc:
        return wrap_fail(exc, "download_file failed")