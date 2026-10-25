"""create_folder tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def create_folder(name: str, parent_id: str | None = None) -> dict[str, Any]:
    """Create a new folder in Drive."""
    try:
        service = _helpers.get_service()
        body: dict[str, Any] = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_id:
            body["parents"] = [parent_id]
        folder = service.files().create(body=body, fields="id,name,parents,webLink").execute()
        return wrap_ok({"folder_id": folder.get("id"), "name": folder.get("name")})
    except Exception as exc:
        return wrap_fail(exc, "create_folder failed")