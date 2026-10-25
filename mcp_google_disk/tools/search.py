"""search tool."""

from __future__ import annotations

from typing import Any

from . import _helpers
from ._helpers import wrap_fail, wrap_ok


async def search(query: str, page_size: int = 20) -> dict[str, Any]:
    """Search Drive files using the Drive query language.

    Example queries:
      - "name contains 'report'"
      - "mimeType contains 'application/pdf'"
      - "modifiedTime > '2024-01-01T00:00:00Z'"
    """
    try:
        service = _helpers.get_service()
        q = f"({query}) and trashed = false"
        request = service.files().list(
            q=q,
            pageSize=max(1, min(page_size, 100)),
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size, parents, webLink)",
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
        return wrap_fail(exc, "search failed")