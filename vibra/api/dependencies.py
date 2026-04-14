from fastapi import Header

from vibra.infrastructure.spotify.auth_manager import SpotifyAuthManager
from vibra.infrastructure.spotify.client import SpotifyClient
from vibra.injections import container


def get_auth_manager() -> SpotifyAuthManager:
    return container.infrastructure.spotify_auth_manager()  # type: ignore[no-any-return]


def get_bearer_token(authorization: str | None = Header(default=None)) -> str | None:
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return

    return parts[1]


def get_spotify_client_for_token(token: str) -> SpotifyClient:
    container.infrastructure.config.spotify.access_token.from_value(token)
    return container.infrastructure.spotify_client()  # type: ignore[no-any-return]
