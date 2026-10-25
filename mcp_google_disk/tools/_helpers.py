"""Shared helpers for Google Drive MCP tools."""

from __future__ import annotations

import base64
import io
import logging
from typing import Any

from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload

from ..auth import GoogleAuth
from ..models import ToolResponse

logger = logging.getLogger(__name__)


def get_service() -> Any:
    """Build a Drive API service from the loaded configuration."""
    from ..config import load_config

    config = load_config()
    auth = GoogleAuth(config)
    return auth.build_service()


def _format_error(exc: Exception, default: str = "Google API error") -> str:
    """Convert common Google API exceptions into readable messages."""
    text = str(exc)
    if "quota" in text.lower():
        return "Google Drive API quota exceeded. Try again later or increase quota."
    if "403" in text or "Forbidden" in text:
        return f"Permission denied: {text}"
    if "404" in text or "NotFound" in text:
        return f"File not found: {text}"
    if "429" in text:
        return f"Rate limit exceeded: {text}"
    return f"{default}: {text}"


def download_to_bytes(service: Any, file_id: str, export_mime_type: str | None = None) -> bytes:
    """Stream a Drive file into memory (bytes).

    If ``export_mime_type`` is provided, the file is exported using the
    Google Docs export API (for Google-native documents such as Docs/Sheets).
    """
    buf = io.BytesIO()
    if export_mime_type:
        request = service.files().export(fileId=file_id, mimeType=export_mime_type)
    else:
        request = service.files().get_media(fileId=file_id)
    downloader = MediaIoBaseDownload(buf, request, chunksize=1024 * 1024)
    done = False
    while not done:
        _status, done = downloader.next_chunk()
    return buf.getvalue()


def upload_from_bytes(
    service: Any,
    name: str,
    content: bytes,
    parent_id: str | None = None,
    mime_type: str | None = None,
) -> dict[str, Any]:
    """Upload bytes to Drive, returning the created file metadata."""
    media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mime_type or "application/octet-stream", resumable=True)
    body: dict[str, Any] = {"name": name}
    if parent_id:
        body["parents"] = [parent_id]
    file = service.files().create(body=body, media_body=media, fields="id,name,parents,webLink").execute()
    return file


def decode_content(content: str | bytes) -> bytes:
    """Decode base64 content if it looks like base64, otherwise encode text."""
    if isinstance(content, bytes):
        return content
    try:
        return base64.b64decode(content)
    except Exception:
        return content.encode("utf-8")


def wrap_ok(data: Any | None = None) -> dict[str, Any]:
    return ToolResponse.ok(data).to_dict()


def wrap_fail(exc: Exception, default: str = "Google API error") -> dict[str, Any]:
    return ToolResponse.fail(_format_error(exc, default)).to_dict()