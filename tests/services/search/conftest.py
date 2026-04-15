import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure.generation.fake import FakeTextGenerator
from vibra.infrastructure.vector_store.fake import FakeVectorStore
from vibra.services import SearchService


@pytest.fixture
def fake_vector_store() -> FakeVectorStore:
    return FakeVectorStore()


@pytest.fixture
def search_service(fake_vector_store: FakeVectorStore) -> SearchService:
    return SearchService(
        vector_store=fake_vector_store,
        text_generator=FakeTextGenerator(),
    )


@pytest.fixture
def sample_query() -> str:
    return "sad melancholic songs about heartbreak"


@pytest.fixture
def _populate_search_tracks(fake_vector_store: FakeVectorStore) -> None:
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

    fake_vector_store.add_tracks(tracks)
