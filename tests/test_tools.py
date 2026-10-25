"""Unit tests for mcp-google-disk tools."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp_google_disk.tools.create_folder import create_folder
from mcp_google_disk.tools.delete_file import delete_file
from mcp_google_disk.tools.download_file import download_file
from mcp_google_disk.tools.get_metadata import get_metadata
from mcp_google_disk.tools.list_files import list_files
from mcp_google_disk.tools.move_file import move_file
from mcp_google_disk.tools.rename_file import rename_file
from mcp_google_disk.tools.search import search
from mcp_google_disk.tools.upload_file import upload_file


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture(autouse=True)
def patch_get_service(monkeypatch, mock_service):
    from mcp_google_disk.tools import _helpers

    monkeypatch.setattr(_helpers, "get_service", lambda: mock_service)
    yield


async def test_list_files_success(mock_service):
    mock_service.files().list().execute.return_value = {
        "files": [{"id": "1", "name": "a.txt"}],
        "nextPageToken": "tok",
    }
    result = await list_files(parent_id="root", page_size=10)
    assert result["success"] is True
    assert result["data"]["files"][0]["name"] == "a.txt"
    assert result["data"]["next_page_token"] == "tok"
    args, kwargs = mock_service.files().list.call_args
    assert "'root' in parents" in kwargs["q"]
    assert "trashed = false" in kwargs["q"]


async def test_list_files_failure(mock_service):
    mock_service.files().list().execute.side_effect = RuntimeError("boom")
    result = await list_files()
    assert result["success"] is False
    assert result["error"] is not None
    assert "list_files failed" in result["error"]


async def test_get_metadata_success(mock_service):
    mock_service.files().get().execute.return_value = {"id": "1", "name": "a.txt", "mimeType": "text/plain"}
    result = await get_metadata(file_id="1")
    assert result["success"] is True
    assert result["data"]["file"]["name"] == "a.txt"


async def test_download_file_success(mock_service, monkeypatch):
    mock_service.files().get().execute.return_value = {"id": "1", "name": "a.txt", "mimeType": "text/plain"}
    monkeypatch.setattr("mcp_google_disk.tools._helpers.download_to_bytes", lambda s, fid, mt: b"hello")
    result = await download_file(file_id="1")
    assert result["success"] is True
    assert result["data"]["name"] == "a.txt"
    assert result["data"]["content_base64"] == "aGVsbG8="


async def test_download_file_with_output_path(mock_service, monkeypatch, tmp_path):
    mock_service.files().get().execute.return_value = {"id": "1", "name": "a.txt", "mimeType": "text/plain"}
    monkeypatch.setattr("mcp_google_disk.tools._helpers.download_to_bytes", lambda s, fid, mt: b"hello")
    out = tmp_path / "a.txt"
    result = await download_file(file_id="1", output_path=str(out))
    assert result["success"] is True
    assert result["data"]["path"] == str(out)
    assert out.read_bytes() == b"hello"


async def test_upload_file_success(mock_service):
    mock_service.files().create().execute.return_value = {
        "id": "1",
        "name": "a.txt",
        "webLink": "https://drive.google.com/file/d/1",
    }
    result = await upload_file(name="a.txt", content="hello")
    assert result["success"] is True
    assert result["data"]["file_id"] == "1"


async def test_create_folder_success(mock_service):
    mock_service.files().create().execute.return_value = {"id": "1", "name": "folder", "parents": []}
    result = await create_folder(name="folder")
    assert result["success"] is True
    assert result["data"]["folder_id"] == "1"


async def test_delete_file_success(mock_service):
    result = await delete_file(file_id="1")
    assert result["success"] is True
    assert result["data"]["deleted"] is True
    mock_service.files().update.assert_called_once()
    assert mock_service.files().update.call_args.kwargs["body"] == {"trashed": True}


async def test_move_file_success(mock_service):
    mock_service.files().get().execute.return_value = {"parents": ["old"]}
    mock_service.files().update().execute.return_value = {"id": "1", "parents": ["new"]}
    result = await move_file(file_id="1", new_parent_id="new")
    assert result["success"] is True
    assert result["data"]["parents"] == ["new"]
    assert mock_service.files().update.call_args.kwargs["addParents"] == "new"
    assert mock_service.files().update.call_args.kwargs["removeParents"] == "old"


async def test_rename_file_success(mock_service):
    mock_service.files().update().execute.return_value = {"id": "1", "name": "new.txt"}
    result = await rename_file(file_id="1", name="new.txt")
    assert result["success"] is True
    assert result["data"]["name"] == "new.txt"


async def test_search_success(mock_service):
    mock_service.files().list().execute.return_value = {
        "files": [{"id": "1", "name": "report.pdf"}],
        "nextPageToken": None,
    }
    result = await search(query="name contains 'report'", page_size=5)
    assert result["success"] is True
    assert result["data"]["files"][0]["name"] == "report.pdf"
    args, kwargs = mock_service.files().list.call_args
    assert "name contains 'report'" in kwargs["q"]
    assert "trashed = false" in kwargs["q"]


async def test_search_failure(mock_service):
    mock_service.files().list().execute.side_effect = RuntimeError("boom")
    result = await search(query="x")
    assert result["success"] is False
    assert "search failed" in result["error"]


def test_wrap_helpers():
    from mcp_google_disk.tools._helpers import wrap_ok, wrap_fail

    ok = wrap_ok({"a": 1})
    assert ok == {"success": True, "data": {"a": 1}, "error": None}

    fail = wrap_fail(RuntimeError("oops"))
    assert fail["success"] is False
    assert fail["data"] is None
    assert "oops" in fail["error"]


def test_decode_content():
    from mcp_google_disk.tools._helpers import decode_content

    assert decode_content("hello") == b"hello"
    assert decode_content(b"raw") == b"raw"
    assert decode_content("aGVsbG8=") == b"hello"