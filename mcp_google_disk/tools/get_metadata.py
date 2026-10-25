"""get_metadata tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def get_metadata(file_id: str, fields: str | None = None) -> dict[str, Any]:
    """Retrieve metadata for a single Drive file."""
    try:
        service = _helpers.get_service()
        actual_fields = fields or "id,name,mimeType,modifiedTime,size,parents,webLink,description,createdTime,viewedByMeTime"
        file = service.files().get(fileId=file_id, fields=actual_fields).execute()
        return wrap_ok({"file": file})
    except Exception as exc:
        return wrap_fail(exc, "get_metadata failed")