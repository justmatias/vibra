# pylint: disable=line-too-long, duplicate-code
import pathlib
from collections.abc import Generator

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure import LLMClient, VectorDBRepository
from vibra.services import SearchService
from vibra.utils import Settings


@pytest.fixture
def vectordb_repository(tmp_path: pathlib.Path) -> Generator[VectorDBRepository]:
    """Fixture providing a VectorDBRepository with temporary storage."""
    original_data_dir = Settings.DATA_DIR
    Settings.DATA_DIR = tmp_path
    yield VectorDBRepository()
    Settings.DATA_DIR = original_data_dir


@pytest.fixture
def llm_client() -> LLMClient:
    return LLMClient()


@pytest.fixture
def search_service(vectordb_repository: VectorDBRepository) -> SearchService:
    return SearchService(
        vectordb_repository=vectordb_repository, llm_client=LLMClient()
    )


@pytest.fixture
def sample_query() -> str:
    return "sad melancholic songs about heartbreak"


@pytest.fixture
def _populate_search_tracks(vectordb_repository: VectorDBRepository) -> None:

    enriched_track_factory = ModelFactory.create_factory(EnrichedTrack)
    saved_track_factory = ModelFactory.create_factory(SavedTrack)

    tracks = [
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="An upbeat pop song with catchy hooks and positive energy perfect for dancing",
            lyrics="Sample lyrics about happiness",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A melancholic indie track with introspective lyrics about lost love and regret",
            lyrics="Sample lyrics about heartbreak",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A dark and heavy metal track with aggressive guitar riffs and intense vocals",
            lyrics="Sample lyrics about anger",
        ),
    ]

    vectordb_repository.add_tracks(tracks)
