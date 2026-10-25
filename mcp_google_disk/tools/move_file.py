"""move_file tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def move_file(file_id: str, new_parent_id: str) -> dict[str, Any]:
    """Move a file into another folder."""
    try:
        service = _helpers.get_service()
        current = service.files().get(fileId=file_id, fields="parents").execute()
        old_parents = current.get("parents", [])
        remove_parents = ",".join([p for p in old_parents if p != new_parent_id])

        update_kwargs: dict[str, Any] = {
            "fileId": file_id,
            "body": {},
            "addParents": new_parent_id,
            "fields": "id,parents",
        }
        if remove_parents:
            update_kwargs["removeParents"] = remove_parents

        file = service.files().update(**update_kwargs).execute()
        return wrap_ok({"file_id": file.get("id"), "parents": file.get("parents", [])})
    except Exception as exc:
        return wrap_fail(exc, "move_file failed")