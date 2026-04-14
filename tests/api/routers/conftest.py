"""Shared fixtures for API router tests."""

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from vibra.api.app import app
from vibra.api.dependencies import get_auth_manager
from vibra.domain import SpotifyUser
from vibra.infrastructure.auth import FakeAuthManager


@pytest.fixture
def fake_token() -> dict[str, Any]:
    return {
        "access_token": "test_access_token",
        "refresh_token": "test_refresh_token",
        "expires_in": 3600,
        "expires_at": 9999999999,
        "scope": "user-library-read",
    }


@pytest.fixture
def api_client() -> TestClient:
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture
def fake_auth_manager(
    fake_token: dict[str, Any]
) -> FakeAuthManager:
    """A pre-configured FakeAuthManager with default happy-path values."""
    return FakeAuthManager(
        access_token=fake_token,
        refresh_token=fake_token,
    )


@pytest.fixture(autouse=True)
def _override_auth_manager(
    fake_auth_manager: FakeAuthManager,
) -> Iterator[None]:
    """Override the auth manager dependency for every test in this package."""
    app.dependency_overrides[get_auth_manager] = lambda: fake_auth_manager
    yield
    app.dependency_overrides.pop(get_auth_manager, None)


@pytest.fixture
def fake_user() -> SpotifyUser:
    return SpotifyUser(
        id="user1",
        display_name="Test User",
        email="test@example.com",
        country="US",
        product="premium",
        image_url=None,
        followers=0,
    )


@pytest.fixture
def mock_spotify_client(fake_user: SpotifyUser) -> MagicMock:
    """A mock SpotifyClient with a default current_user."""
    mock = MagicMock()
    mock.current_user = fake_user
    return mock


@pytest.fixture
def override_cache_path(tmp_path: Path) -> Iterator[Path]:
    """Patch Settings.CACHE_PATH to a temporary directory for logout tests."""
    with patch("vibra.api.routers.auth.Settings") as mock_settings:
        mock_settings.CACHE_PATH = tmp_path
        yield tmp_path
