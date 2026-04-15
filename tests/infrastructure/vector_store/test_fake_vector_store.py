from vibra.domain import EnrichedTrack
from vibra.infrastructure.vector_store.fake import FakeVectorStore


def test_delete_tracks_removes_existing(
    fake_vector_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    fake_vector_store.add_track(track_with_vibe)
    assert fake_vector_store.track_exists(track_with_vibe.track_id)

    fake_vector_store.delete_tracks([track_with_vibe.track_id])

    assert not fake_vector_store.track_exists(track_with_vibe.track_id)


def test_delete_tracks_ignores_missing_ids(fake_vector_store: FakeVectorStore) -> None:
    fake_vector_store.delete_tracks(["nonexistent_id"])

    assert fake_vector_store.count_tracks() == 0


def test_get_all_tracks_returns_all(
    fake_vector_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    fake_vector_store.add_track(track_with_vibe)

    result = fake_vector_store.get_all_tracks()

    assert track_with_vibe.track_id in result["ids"]
    assert track_with_vibe.vibe_description in result["documents"]
    assert len(result["metadatas"]) == 1


def test_count_tracks_reflects_stored_tracks(
    fake_vector_store: FakeVectorStore,
    track_with_vibe: EnrichedTrack,
) -> None:
    assert fake_vector_store.count_tracks() == 0

    fake_vector_store.add_track(track_with_vibe)

    assert fake_vector_store.count_tracks() == 1
