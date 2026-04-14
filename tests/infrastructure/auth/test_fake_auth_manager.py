from typing import Any

import pytest

from vibra.domain import AuthManager
from vibra.infrastructure.auth import FakeAuthManager

SAMPLE_TOKEN: dict[str, Any] = {
    "access_token": "fake_access_token",
    "refresh_token": "fake_refresh_token",
    "expires_in": 3600,
}


def test_fake_auth_manager_satisfies_protocol() -> None:
    manager = FakeAuthManager()
    assert isinstance(manager, AuthManager)


def test_get_auth_url_returns_default() -> None:
    manager = FakeAuthManager()
    url = manager.get_auth_url()

    assert "accounts.spotify.com" in url


def test_get_auth_url_returns_custom() -> None:
    custom_url = "https://custom.auth/authorize"
    manager = FakeAuthManager(auth_url=custom_url)

    assert manager.get_auth_url() == custom_url


def test_get_access_token_returns_none_by_default() -> None:
    manager = FakeAuthManager()

    assert manager.get_access_token("any_code") is None


def test_get_access_token_returns_configured_token() -> None:
    manager = FakeAuthManager(access_token=SAMPLE_TOKEN)

    result = manager.get_access_token("any_code")

    assert result == SAMPLE_TOKEN
    assert result is not None
    assert result["access_token"] == "fake_access_token"


def test_get_access_token_ignores_code_value() -> None:
    manager = FakeAuthManager(access_token=SAMPLE_TOKEN)

    assert manager.get_access_token("code_a") == manager.get_access_token("code_b")


def test_get_cached_token_returns_none_by_default() -> None:
    manager = FakeAuthManager()

    assert manager.get_cached_token() is None


def test_get_cached_token_returns_configured_token() -> None:
    manager = FakeAuthManager(cached_token=SAMPLE_TOKEN)

    assert manager.get_cached_token() == SAMPLE_TOKEN


def test_refresh_token_returns_none_by_default() -> None:
    manager = FakeAuthManager()

    assert manager.refresh_token("any_refresh") is None


def test_refresh_token_returns_configured_token() -> None:
    manager = FakeAuthManager(refresh_token=SAMPLE_TOKEN)

    result = manager.refresh_token("any_refresh")

    assert result == SAMPLE_TOKEN


@pytest.mark.parametrize(
    ("field", "kwarg"),
    [
        ("access_token", "access_token"),
        ("refresh_token", "refresh_token"),
        ("cached_token", "cached_token"),
    ],
)
def test_none_simulates_failure(field: str, kwarg: str) -> None:
    manager = FakeAuthManager(**{kwarg: None})

    method_map = {
        "access_token": lambda: manager.get_access_token("code"),
        "refresh_token": lambda: manager.refresh_token("token"),
        "cached_token": lambda: manager.get_cached_token(),
    }

    assert method_map[field]() is None
