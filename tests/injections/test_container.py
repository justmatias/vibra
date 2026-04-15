from vibra.infrastructure import GeniusClient, SpotifyClient
from vibra.injections import Container, container
from vibra.services import LibrarySyncService


def test_container_initialization() -> None:
    container = Container()
    assert container


def test_singleton_container_exists() -> None:
    assert container


def test_library_client_creation() -> None:
    container.infrastructure.config.spotify.access_token.from_value("test_token")

    client = container.infrastructure.library_client()
    assert isinstance(client, SpotifyClient)


def test_lyrics_client_creation() -> None:
    client = container.infrastructure.lyrics_client()
    assert isinstance(client, GeniusClient)


def test_library_sync_service_creation() -> None:
    container.infrastructure.config.spotify.access_token.from_value("test_token")

    service = container.services.library_sync_service()
    assert isinstance(service, LibrarySyncService)
