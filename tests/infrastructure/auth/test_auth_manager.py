from unittest.mock import MagicMock

import pytest

from vibra.infrastructure import SpotifyAuthManager


@pytest.mark.usefixtures("setup_get_auth_url")
def test_auth_manager_get_auth_url(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    url = auth_manager.get_auth_url()

    assert url == "http://auth.url"
    mock_oauth_instance.get_authorize_url.assert_called_once()


@pytest.mark.usefixtures("setup_get_access_token_success")
def test_auth_manager_get_access_token_success(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = auth_manager.get_access_token("code")
    assert token == {"access_token": "123"}
    mock_oauth_instance.get_access_token.assert_called_with("code", as_dict=True)


@pytest.mark.usefixtures("setup_get_access_token_failure")
def test_auth_manager_get_access_token_failure(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = auth_manager.get_access_token("code_fail")
    assert token is None


@pytest.mark.usefixtures("setup_refresh_token_success")
def test_auth_manager_refresh_token_success(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = auth_manager.refresh_token("refresh_code")
    assert token == {"access_token": "new_123"}
    mock_oauth_instance.refresh_access_token.assert_called_with("refresh_code")


@pytest.mark.usefixtures("setup_refresh_token_failure")
def test_auth_manager_refresh_token_failure(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = auth_manager.refresh_token("refresh_code_fail")
    assert token is None


@pytest.mark.usefixtures("setup_get_cached_token_missing")
def test_auth_manager_get_cached_token_missing(
    auth_manager: SpotifyAuthManager,
) -> None:
    token = auth_manager.get_cached_token()
    assert token is None


@pytest.mark.usefixtures("setup_get_cached_token_valid")
def test_auth_manager_get_cached_token_valid(
    auth_manager: SpotifyAuthManager,
    mock_oauth_instance: MagicMock,
) -> None:
    token = auth_manager.get_cached_token()
    assert token == {"access_token": "cached"}
    mock_oauth_instance.validate_token.assert_called_with({"access_token": "cached"})
