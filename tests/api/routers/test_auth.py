from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from vibra.api.app import app
from vibra.api.dependencies import get_auth_manager
from vibra.infrastructure.auth import FakeAuthManager


def test_authorize_returns_spotify_url(api_client: TestClient) -> None:
    response = api_client.get("/api/auth/authorize")

    assert response.status_code == 200
    assert "accounts.spotify.com" in response.json()["auth_url"]


def test_callback_returns_token_on_success(
    api_client: TestClient, fake_token: dict[str, Any]
) -> None:
    response = api_client.post("/api/auth/callback", json={"code": "auth_code_123"})

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == fake_token.get("access_token")
    assert data["refresh_token"] == fake_token.get("refresh_token")
    assert data["token_type"] == "Bearer"


def test_callback_returns_401_when_exchange_fails(api_client: TestClient) -> None:
    app.dependency_overrides[get_auth_manager] = lambda: FakeAuthManager(
        access_token=None
    )

    response = api_client.post("/api/auth/callback", json={"code": "bad_code"})

    assert response.status_code == 401


def test_refresh_returns_new_token(
    api_client: TestClient,
    fake_token: dict[str, Any],
) -> None:
    response = api_client.post(
        "/api/auth/refresh", json={"refresh_token": "old_refresh"}
    )

    assert response.status_code == 200
    assert response.json()["access_token"] == fake_token.get("access_token")


def test_refresh_returns_401_when_refresh_fails(api_client: TestClient) -> None:
    app.dependency_overrides[get_auth_manager] = lambda: FakeAuthManager(
        refresh_token=None
    )

    response = api_client.post(
        "/api/auth/refresh", json={"refresh_token": "bad_refresh"}
    )

    assert response.status_code == 401


def test_logout_deletes_cache_file(
    api_client: TestClient, override_cache_path: Path
) -> None:
    cache_file = override_cache_path / ".spotify_cache"
    cache_file.write_text('{"access_token": "cached"}')

    response = api_client.post("/api/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"cleared": True}
    assert not cache_file.exists()


def test_logout_idempotent_when_no_cache(
    api_client: TestClient,
    override_cache_path: Path,  # pylint: disable=unused-argument
) -> None:
    response = api_client.post("/api/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"cleared": False}


def test_me_returns_user_for_bearer_token(
    api_client: TestClient,
    mock_spotify_client: MagicMock,
) -> None:
    with patch(
        "vibra.api.routers.auth.get_spotify_client_for_token",
        return_value=mock_spotify_client,
    ):
        response = api_client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer test_access_token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "user1"
    assert data["display_name"] == "Test User"


def test_me_returns_401_when_no_token(api_client: TestClient) -> None:
    response = api_client.get("/api/auth/me")

    assert response.status_code == 401


@pytest.mark.parametrize(
    "bad_header",
    [
        "InvalidFormat",
        "Basic dXNlcjpwYXNz",
        "Bearer",
        "",
    ],
    ids=["no-scheme", "wrong-scheme", "missing-value", "empty"],
)
def test_me_returns_401_for_malformed_authorization(
    api_client: TestClient, bad_header: str
) -> None:
    response = api_client.get(
        "/api/auth/me",
        headers={"Authorization": bad_header},
    )

    assert response.status_code == 401
