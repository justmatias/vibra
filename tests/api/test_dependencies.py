from vibra.api.dependencies import get_auth_manager, get_spotify_client_for_token
from vibra.domain import AuthManager
from vibra.infrastructure import SpotifyClient


def test_get_auth_manager_returns_auth_manager() -> None:
    manager = get_auth_manager()

    assert isinstance(manager, AuthManager)


def test_get_spotify_client_for_token_returns_spotify_client() -> None:
    client = get_spotify_client_for_token("test_token")

    assert isinstance(client, SpotifyClient)
