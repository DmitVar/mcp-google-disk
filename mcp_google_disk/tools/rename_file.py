"""rename_file tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def rename_file(file_id: str, name: str) -> dict[str, Any]:
    """Rename a Drive file."""
    try:
        service = _helpers.get_service()
        file = service.files().update(fileId=file_id, body={"name": name}, fields="id,name").execute()
        return wrap_ok({"file_id": file.get("id"), "name": file.get("name")})
    except Exception as exc:
        return wrap_fail(exc, "rename_file failed")