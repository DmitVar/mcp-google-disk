"""delete_file tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def delete_file(file_id: str) -> dict[str, Any]:
    """Move a file to the trash."""
    try:
        service = _helpers.get_service()
        service.files().update(fileId=file_id, body={"trashed": True}).execute()
        return wrap_ok({"deleted": True, "file_id": file_id})
    except Exception as exc:
        return wrap_fail(exc, "delete_file failed")