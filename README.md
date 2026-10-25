# mcp-google-disk

MCP server for [Google Drive](https://drive.google.com) — exposes 9 tools for listing, downloading, uploading, searching and managing files over the Model Context Protocol.

## Features

- `list_files` — list files in a folder with pagination and Drive query syntax
- `get_metadata` — retrieve metadata for a single file
- `download_file` — stream a file's content (with optional Google-native export)
- `upload_file` — upload a new file
- `create_folder` — create a new folder
- `delete_file` — move a file to the trash
- `move_file` — move a file between folders
- `rename_file` — rename a file
- `search` — search Drive using the Drive query language

## Requirements

- Python 3.10+
- A Google Cloud project with the **Google Drive API** enabled
- OAuth 2.0 credentials with a `refresh_token` (scope: `drive`)

## Installation

```bash
git clone <repo> ~/mcp-google-disk
cd ~/mcp-google-disk
python -m venv .venv
.venv/bin/pip install -e .
```

## Configuration

1. Copy the example config and fill in your secrets:

```bash
cp mcp-google-disk-config.example.json mcp-google-disk-config.json
```

2. Edit `mcp-google-disk-config.json`:

```json
{
  "google": {
    "client_id": "your-client-id.apps.googleusercontent.com",
    "client_secret": "your-client-secret",
    "refresh_token": "your-refresh-token",
    "scopes": ["https://www.googleapis.com/auth/drive"]
  },
  "server": {
    "name": "mcp-google-disk",
    "version": "1.0.0"
  }
}
```

3. The config file **must not** be committed to version control. The path can also be overridden with the `GOOGLE_DISK_CONFIG_PATH` environment variable.

## Usage

Add the server to your MCP host configuration (e.g. `~/.config/claude_desktop/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google-disk": {
      "command": "/home/<user>/mcp-google-disk/.venv/bin/python",
      "args": ["-m", "mcp_google_disk.server"]
    }
  }
}
```

Restart your MCP host and the tools will be available.

## Development

```bash
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## License

MIT