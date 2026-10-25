"""MCP server entry point for Google Drive operations."""

from __future__ import annotations

import json
import logging
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer

from .config import load_config
from .tools.create_folder import create_folder
from .tools.delete_file import delete_file
from .tools.download_file import download_file
from .tools.get_metadata import get_metadata
from .tools.list_files import list_files
from .tools.move_file import move_file
from .tools.rename_file import rename_file
from .tools.search import search
from .tools.upload_file import upload_file

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)


def _make_server() -> MCPServer:
    """Create and configure the MCP server with all Drive tools."""
    config = load_config()
    server = MCPServer(
        name=config.server.name,
        version=config.server.version,
        description="MCP server for Google Drive operations",
        instructions=(
            "Tools for reading, writing, searching and managing files on Google Drive. "
            "All responses are JSON objects with 'success', 'data' and 'error' fields."
        ),
    )

    server.add_tool(
        list_files,
        name="list_files",
        description="List files in a Google Drive folder. Supports pagination and Drive query syntax.",
    )
    server.add_tool(
        get_metadata,
        name="get_metadata",
        description="Retrieve metadata for a single Google Drive file by ID.",
    )
    server.add_tool(
        download_file,
        name="download_file",
        description="Download a Drive file's content. Supports exporting Google-native formats (Docs, Sheets, etc.).",
    )
    server.add_tool(
        upload_file,
        name="upload_file",
        description="Upload a new file to Drive. Content can be text or base64-encoded bytes.",
    )
    server.add_tool(
        create_folder,
        name="create_folder",
        description="Create a new folder in Google Drive.",
    )
    server.add_tool(
        delete_file,
        name="delete_file",
        description="Move a file to the trash.",
    )
    server.add_tool(
        move_file,
        name="move_file",
        description="Move a file from its current folder to a new parent folder.",
    )
    server.add_tool(
        rename_file,
        name="rename_file",
        description="Rename an existing Drive file.",
    )
    server.add_tool(
        search,
        name="search",
        description="Search Drive files using the Drive query language.",
    )
    return server


def main() -> None:
    """Run the MCP server over stdio."""
    try:
        server = _make_server()
    except Exception as exc:
        # Config errors should be reported before the server starts
        print(f"Failed to initialize MCP server: {exc}", file=sys.stderr)
        sys.exit(1)

    import asyncio

    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()