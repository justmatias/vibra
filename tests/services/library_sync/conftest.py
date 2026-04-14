import pathlib
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import (
    EnrichedTrack,
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
)
from vibra.infrastructure import SpotifyClient, VectorDBRepository
from vibra.injections import container
from vibra.services import LibrarySyncService, TrackAnalysisService
from vibra.utils import Settings


@pytest.fixture
def track_analysis_service() -> TrackAnalysisService:
    return container.services.track_analysis_service()  # type: ignore[no-any-return]


@pytest.fixture
def vectordb_repository(tmp_path: pathlib.Path) -> Generator[VectorDBRepository]:
    original_data_dir = Settings.DATA_DIR
    Settings.DATA_DIR = tmp_path
    yield VectorDBRepository()
    Settings.DATA_DIR = original_data_dir


@pytest.fixture
def _populate_tracks(
    vectordb_repository: VectorDBRepository,
    realistic_liked_songs: list[SavedTrack],
    enriched_track_factory: ModelFactory[EnrichedTrack],
) -> None:
    saved_track = realistic_liked_songs[1]  # Stairway to Heaven
    enriched_track = enriched_track_factory.build(
        track=saved_track,
        vibe_description="Existing vibe description",
        has_lyrics=True,
    )
    vectordb_repository.add_track(enriched_track)


@pytest.fixture
def enriched_track_with_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    track = saved_track_factory.build()
    return enriched_track_factory.build(
        track=track,
        lyrics="Test lyrics content",
        has_lyrics=True,
    )


@pytest.fixture
def enriched_track_without_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    track = saved_track_factory.build()
    return enriched_track_factory.build(
        track=track,
        lyrics="",
        has_lyrics=False,
    )


@pytest.fixture
def liked_songs(
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[SavedTrack]:
    return [saved_track_factory.build() for _ in range(3)]


@pytest.fixture
def liked_songs_lyrics(
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[SavedTrack]:
    return [saved_track_factory.build() for _ in range(3)]


@pytest.fixture
def realistic_liked_songs(
    saved_track_factory: ModelFactory[SavedTrack],
    spotify_track_factory: ModelFactory[SpotifyTrack],
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
) -> list[SavedTrack]:
    return [
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Bohemian Rhapsody",
                artists=[
                    spotify_artist_factory.build(
                        name="Queen", genres=["rock", "classic rock"]
                    )
                ],
                album=spotify_album_factory.build(name="A Night at the Opera"),
                popularity=95,
            )
        ),
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Stairway to Heaven",
                artists=[
                    spotify_artist_factory.build(
                        name="Led Zeppelin", genres=["rock", "hard rock"]
                    )
                ],
                album=spotify_album_factory.build(name="Led Zeppelin IV"),
                popularity=92,
            )
        ),
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Hotel California",
                artists=[
                    spotify_artist_factory.build(
                        name="Eagles", genres=["rock", "country rock"]
                    )
                ],
                album=spotify_album_factory.build(name="Hotel California"),
                popularity=90,
            )
        ),
    ]


@pytest.fixture
def mock_spotify_client(
    realistic_liked_songs: list[SavedTrack],
) -> MagicMock:
    client = MagicMock(spec=SpotifyClient)
    client.get_all_liked_songs.return_value = realistic_liked_songs
    return client


@pytest.fixture
def library_sync_service(
    mock_spotify_client: MagicMock,
    vectordb_repository: VectorDBRepository,
) -> LibrarySyncService:
    return LibrarySyncService(
        spotify_client=mock_spotify_client,
        genius_client=container.infrastructure.genius_client(),
        track_analysis_service=container.services.track_analysis_service(),
        vectordb_repository=vectordb_repository,
    )
