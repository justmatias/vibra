import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import (
    EnrichedTrack,
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
)
from vibra.infrastructure.generation.fake import FakeTextGenerator
from vibra.infrastructure.library.fake import FakeLibrary
from vibra.infrastructure.lyrics.fake import FakeLyricsProvider
from vibra.infrastructure.vector_store.fake import FakeVectorStore
from vibra.services import LibrarySyncService, TrackAnalysisService


@pytest.fixture
def fake_text_generator() -> FakeTextGenerator:
    return FakeTextGenerator()


@pytest.fixture
def fake_lyrics_provider() -> FakeLyricsProvider:
    return FakeLyricsProvider()


@pytest.fixture
def fake_vector_store() -> FakeVectorStore:
    return FakeVectorStore()


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
def fake_library(realistic_liked_songs: list[SavedTrack]) -> FakeLibrary:
    return FakeLibrary(liked_songs=realistic_liked_songs)


@pytest.fixture
def library_sync_service(
    fake_library: FakeLibrary,
    fake_lyrics_provider: FakeLyricsProvider,
    fake_text_generator: FakeTextGenerator,
    fake_vector_store: FakeVectorStore,
) -> LibrarySyncService:
    return LibrarySyncService(
        library=fake_library,
        lyrics_provider=fake_lyrics_provider,
        track_analysis_service=TrackAnalysisService(text_generator=fake_text_generator),
        vector_store=fake_vector_store,
    )


@pytest.fixture
def _populate_tracks(
    fake_vector_store: FakeVectorStore,
    realistic_liked_songs: list[SavedTrack],
    enriched_track_factory: ModelFactory[EnrichedTrack],
) -> None:
    saved_track = realistic_liked_songs[1]  # Stairway to Heaven
    enriched_track = enriched_track_factory.build(
        track=saved_track,
        vibe_description="Existing vibe description",
        lyrics="Some lyrics",
    )
    fake_vector_store.add_track(enriched_track)


@pytest.fixture
def enriched_track_with_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    track = saved_track_factory.build()
    return enriched_track_factory.build(
        track=track,
        lyrics="Test lyrics content",
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
        vibe_description=None,
    )
