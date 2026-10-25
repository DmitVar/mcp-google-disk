"""Configuration loader for mcp-google-disk."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class GoogleConfig(BaseModel):
    client_id: str
    client_secret: str
    refresh_token: str
    scopes: list[str] = Field(
        default_factory=lambda: ["https://www.googleapis.com/auth/drive"]
    )


class ServerConfig(BaseModel):
    name: str = "mcp-google-disk"
    version: str = "1.0.0"


class Config(BaseModel):
    google: GoogleConfig
    server: ServerConfig = Field(default_factory=ServerConfig)


def load_config(path: str | None = None) -> Config:
    """Load configuration from a JSON file.

    Path resolution order:
      1. Explicit argument
      2. GOOGLE_DISK_CONFIG_PATH environment variable
      3. ./mcp-google-disk-config.json (current working directory)
    """
    config_path = Path(path or os.getenv("GOOGLE_DISK_CONFIG_PATH", "mcp-google-disk-config.json"))
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}. "
            "Set GOOGLE_DISK_CONFIG_PATH or create the config file."
        )

    with config_path.open("r", encoding="utf-8") as fh:
        raw: dict[str, Any] = json.load(fh)

    try:
        return Config.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid configuration: {exc}") from exc