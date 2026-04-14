"""In-memory fake that satisfies the AuthManager protocol.

All behaviour is controlled via constructor arguments — no mocks needed.
To simulate failures, pass ``None`` for the relevant token parameter.
"""

from typing import Any

from vibra.domain import AuthManager


class FakeAuthManager(AuthManager):
    """Lightweight test double for any AuthManager consumer."""

    def __init__(
        self,
        *,
        auth_url: str = "https://accounts.spotify.com/authorize?client_id=test",
        access_token: dict[str, Any] | None = None,
        refresh_token: dict[str, Any] | None = None,
        cached_token: dict[str, Any] | None = None,
    ) -> None:
        self._auth_url = auth_url
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._cached_token = cached_token

    def get_auth_url(self) -> str:
        return self._auth_url

    def get_access_token(self, code: str) -> dict[str, Any] | None:
        return self._access_token

    def get_cached_token(self) -> dict[str, Any] | None:
        return self._cached_token

    def refresh_token(self, refresh_token: str) -> dict[str, Any] | None:
        return self._refresh_token
