from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AuthManager(Protocol):
    """Protocol that any auth manager implementation must satisfy.

    The production implementation is ``SpotifyAuthManager``; tests can
    inject a lightweight ``FakeAuthManager`` without any external dependencies.
    """

    def get_auth_url(self) -> str: ...

    def get_access_token(self, code: str) -> dict[str, Any] | None: ...

    def get_cached_token(self) -> dict[str, Any] | None: ...

    def refresh_token(self, refresh_token: str) -> dict[str, Any] | None: ...
