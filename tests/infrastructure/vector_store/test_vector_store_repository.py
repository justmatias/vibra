# pylint: disable=protected-access
import pytest

from vibra.domain import EnrichedTrack
from vibra.infrastructure import VectorDBRepository


def test_client_lazy_loading(
    vectordb_repository: VectorDBRepository,
) -> None:
    assert vectordb_repository._client is None
    client = vectordb_repository.client
    assert vectordb_repository._client is client


def test_collection_creation(
    vectordb_repository: VectorDBRepository,
) -> None:
    collection = vectordb_repository.collection
    assert collection.name == "tracks"


@pytest.mark.vcr
def test_add_track_with_vibe_description(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_track(enriched_track_with_vibe)

    assert vectordb_repository.collection.count() == initial_count + 1
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1
    assert result["ids"][0] == enriched_track_with_vibe.track_id
    assert result["metadatas"][0]["track_id"] == enriched_track_with_vibe.track_id


def test_add_track_without_vibe_skips(
    vectordb_repository: VectorDBRepository,
    enriched_track_without_vibe: EnrichedTrack,
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_track(enriched_track_without_vibe)

    assert vectordb_repository.collection.count() == initial_count


@pytest.mark.vcr
def test_add_tracks_batch(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    initial_count = vectordb_repository.collection.count()
    vectordb_repository.add_tracks(enriched_tracks_batch)
    assert vectordb_repository.collection.count() == initial_count + 2


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_single_track")
def test_delete_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 1

    vectordb_repository.delete_tracks([enriched_track_with_vibe.track_id])
    result = vectordb_repository.collection.get(ids=[enriched_track_with_vibe.track_id])
    assert len(result["ids"]) == 0


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
def test_delete_multiple_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    track_ids = [
        track.track_id for track in enriched_tracks_batch if track.vibe_description
    ]

    vectordb_repository.delete_tracks(track_ids)
    result = vectordb_repository.collection.get(ids=track_ids)

    assert len(result["ids"]) == 0


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
def test_search_by_vibe_finds_matching_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.search_by_vibe(
        "sad songs about heartbreak", n_results=3
    )

    assert "ids" in results
    assert "documents" in results
    assert "metadatas" in results
    assert "distances" in results

    assert len(results["ids"][0]) > 0
    assert len(results["documents"][0]) > 0


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
def test_search_by_vibe_returns_correct_number_of_results(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.search_by_vibe("energetic music", n_results=2)

    assert len(results["ids"][0]) <= 2


@pytest.mark.vcr
def test_search_by_vibe_empty_collection(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.search_by_vibe("any query", n_results=10)

    assert len(results["ids"][0]) == 0
    assert len(results["documents"][0]) == 0


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_search_tracks")
def test_search_by_vibe_returns_metadata(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.search_by_vibe("happy upbeat songs", n_results=3)

    if len(results["metadatas"][0]) > 0:
        metadata = results["metadatas"][0][0]
        assert "track_id" in metadata
        assert "track_name" in metadata
        assert "artist_names" in metadata
        assert "album_name" in metadata


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
def test_get_all_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    results = vectordb_repository.get_all_tracks()
    assert len(results["ids"]) > 0


@pytest.mark.vcr
@pytest.mark.usefixtures("_populate_with_batch")
def test_count_tracks(
    vectordb_repository: VectorDBRepository,
) -> None:
    count = vectordb_repository.count_tracks()
    assert count > 0


def test_count_tracks_empty(
    vectordb_repository: VectorDBRepository,
) -> None:
    count = vectordb_repository.count_tracks()
    assert count == 0


def test_add_tracks_with_no_valid_tracks_is_noop(
    vectordb_repository: VectorDBRepository,
    enriched_track_without_vibe: EnrichedTrack,
) -> None:
    vectordb_repository.add_tracks([enriched_track_without_vibe])

    assert vectordb_repository.count_tracks() == 0


@pytest.mark.vcr
def test_track_exists(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    assert not vectordb_repository.track_exists(enriched_track_with_vibe.track_id)

    vectordb_repository.add_track(enriched_track_with_vibe)

    assert vectordb_repository.track_exists(enriched_track_with_vibe.track_id)
