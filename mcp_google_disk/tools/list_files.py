"""list_files tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def list_files(
    parent_id: str | None = None,
    page_size: int = 20,
    query: str | None = None,
) -> dict[str, Any]:
    """List files in a Drive folder with optional pagination and query."""
    try:
        service = _helpers.get_service()
        q_parts: list[str] = []
        if parent_id:
            q_parts.append(f"'{parent_id}' in parents")
        if query:
            q_parts.append(query)
        q = " and ".join(q_parts) + " and trashed = false" if q_parts else "trashed = false"

        request = service.files().list(
            q=q,
            pageSize=max(1, min(page_size, 100)),
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents, webViewLink)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        )
        result = request.execute()
        return wrap_ok(
            {
                "files": result.get("files", []),
                "next_page_token": result.get("nextPageToken"),
            }
        )
    except Exception as exc:
        return wrap_fail(exc, "list_files failed")