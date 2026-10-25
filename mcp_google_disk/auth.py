"""OAuth2 authentication helpers for Google Drive."""

from __future__ import annotations

import logging
from typing import Any

from google.auth.exceptions import RefreshError
from google.auth.transport import requests as google_requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .config import Config

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleAuth:
    """Manages OAuth2 credentials and Drive API client construction."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._credentials: Credentials | None = None

    def get_credentials(self) -> Credentials:
        """Return valid credentials, refreshing the token if necessary."""
        google = self._config.google
        creds = Credentials(
            token=None,
            refresh_token=google.refresh_token,
            client_id=google.client_id,
            client_secret=google.client_secret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=google.scopes or SCOPES,
        )
        if not creds.valid:
            try:
                request = google_requests.Request()
                creds.refresh(request)
            except RefreshError as exc:
                raise RuntimeError(
                    "Failed to refresh Google OAuth token. Check client_id, "
                    "client_secret and refresh_token in the config."
                ) from exc
        self._credentials = creds
        return creds

    def build_service(self) -> Any:
        """Build and return a Drive API service object."""
        creds = self.get_credentials()
        return build("drive", "v3", credentials=creds, cache_discovery=False)