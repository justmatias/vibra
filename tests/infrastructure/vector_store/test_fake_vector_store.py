from polyfactory.factories.pydantic_factory import ModelFactory

import pytest

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure.vector_store.fake import FakeVectorStore


@pytest.fixture
def fake_store() -> FakeVectorStore:
    return FakeVectorStore()


@pytest.fixture
def track_with_vibe(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        track=saved_track_factory.build(),
        vibe_description="A lively pop track",
        lyrics="some lyrics",
    )


def test_delete_tracks_removes_existing(
    fake_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    fake_store.add_track(track_with_vibe)
    assert fake_store.track_exists(track_with_vibe.track_id)

    fake_store.delete_tracks([track_with_vibe.track_id])

    assert not fake_store.track_exists(track_with_vibe.track_id)


def test_delete_tracks_ignores_missing_ids(fake_store: FakeVectorStore) -> None:
    fake_store.delete_tracks(["nonexistent_id"])

    assert fake_store.count_tracks() == 0


def test_get_all_tracks_returns_all(
    fake_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    fake_store.add_track(track_with_vibe)

    result = fake_store.get_all_tracks()

    assert track_with_vibe.track_id in result["ids"]
    assert track_with_vibe.vibe_description in result["documents"]
    assert len(result["metadatas"]) == 1


def test_count_tracks_reflects_stored_tracks(
    fake_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    assert fake_store.count_tracks() == 0

    fake_store.add_track(track_with_vibe)

    assert fake_store.count_tracks() == 1
