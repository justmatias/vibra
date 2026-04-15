from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from spotipy.oauth2 import SpotifyOauthError

from vibra.infrastructure.auth import SpotifyAuthManager


@pytest.fixture
def mock_spotify_oauth() -> Generator[MagicMock, None, None]:
    with patch(
        "vibra.infrastructure.auth.spotify.SpotifyOAuth"
    ) as mock_cls:
        yield mock_cls


@pytest.fixture
def mock_oauth_instance(mock_spotify_oauth: MagicMock) -> MagicMock:
    return mock_spotify_oauth.return_value  # type: ignore[no-any-return]


@pytest.fixture
def auth_manager(mock_oauth_instance: MagicMock) -> SpotifyAuthManager:
    auth_manager = SpotifyAuthManager()
    auth_manager.__dict__["oauth"] = mock_oauth_instance
    return auth_manager


@pytest.fixture
def setup_get_auth_url(mock_oauth_instance: MagicMock) -> None:
    mock_oauth_instance.get_authorize_url.return_value = "http://auth.url"


@pytest.fixture
def setup_get_access_token_success(mock_oauth_instance: MagicMock) -> None:
    expected_token = {"access_token": "123"}
    mock_oauth_instance.get_access_token.return_value = expected_token


@pytest.fixture
def setup_get_access_token_failure(mock_oauth_instance: MagicMock) -> None:
    mock_oauth_instance.get_access_token.side_effect = SpotifyOauthError("Error")


@pytest.fixture
def setup_refresh_token_success(mock_oauth_instance: MagicMock) -> None:
    expected_token = {"access_token": "new_123"}
    mock_oauth_instance.refresh_access_token.return_value = expected_token


@pytest.fixture
def setup_refresh_token_failure(mock_oauth_instance: MagicMock) -> None:
    mock_oauth_instance.refresh_access_token.side_effect = SpotifyOauthError("Error")


@pytest.fixture
def setup_get_cached_token_missing(mock_oauth_instance: MagicMock) -> None:
    mock_oauth_instance.cache_handler.get_cached_token.return_value = None


@pytest.fixture
def setup_get_cached_token_valid(mock_oauth_instance: MagicMock) -> None:
    token_info = {"access_token": "cached"}
    mock_oauth_instance.cache_handler.get_cached_token.return_value = token_info
    mock_oauth_instance.validate_token.return_value = token_info
