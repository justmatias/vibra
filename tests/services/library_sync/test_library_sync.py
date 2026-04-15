import pytest

from vibra.domain import EnrichedTrack, SyncProgress
from vibra.infrastructure import FakeLibrary
from vibra.services import LibrarySyncService


def test_sync_library_yields_progress_and_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    assert isinstance(results[0], SyncProgress)
    assert isinstance(results[1], EnrichedTrack)


def test_sync_library_progress_increments(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    progress_updates = [r for r in results if isinstance(r, SyncProgress)]

    assert len(progress_updates) == 3
    assert progress_updates[0].current == 1
    assert progress_updates[1].current == 2
    assert progress_updates[2].current == 3
    assert all(p.total == 3 for p in progress_updates)


def test_sync_library_tracks_with_and_without_lyrics(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    enriched_tracks = [
        result for result in results if isinstance(result, EnrichedTrack)
    ]

    assert len(enriched_tracks) == 3

    assert enriched_tracks[0].has_lyrics
    assert "Bohemian Rhapsody" in enriched_tracks[0].track.track.name

    assert enriched_tracks[1].has_lyrics
    assert enriched_tracks[2].has_lyrics


def test_sync_library_calls_library(
    library_sync_service: LibrarySyncService,
    fake_library: FakeLibrary,
) -> None:
    list(library_sync_service.sync_library(limit=5))

    assert len(fake_library.get_all_liked_songs_calls) == 1
    assert fake_library.get_all_liked_songs_calls[0]["max_tracks"] == 5


def test_sync_library_fetches_lyrics_for_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    enriched_tracks = [r for r in results if isinstance(r, EnrichedTrack)]
    assert len(enriched_tracks) == 3
    assert all(t.has_lyrics for t in enriched_tracks)


def test_enriched_track_properties(
    enriched_track_with_lyrics: EnrichedTrack,
    enriched_track_without_lyrics: EnrichedTrack,
) -> None:
    assert enriched_track_with_lyrics.has_lyrics
    assert len(enriched_track_with_lyrics.lyrics) > 0
    assert enriched_track_with_lyrics.track

    assert not enriched_track_without_lyrics.has_lyrics
    assert not enriched_track_without_lyrics.lyrics


@pytest.mark.usefixtures("_populate_tracks")
def test_sync_library_skips_existing_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    progress_updates = [r for r in results if isinstance(r, SyncProgress)]
    assert len(progress_updates) == 3

    enriched_tracks = [r for r in results if isinstance(r, EnrichedTrack)]
    assert len(enriched_tracks) == 2
