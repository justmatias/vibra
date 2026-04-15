import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import SavedTrack
from vibra.infrastructure.generation.fake import FakeTextGenerator
from vibra.services import TrackAnalysisService


@pytest.fixture
def fake_text_generator() -> FakeTextGenerator:
    return FakeTextGenerator()


@pytest.fixture
def track_analysis_service(fake_text_generator: FakeTextGenerator) -> TrackAnalysisService:
    return TrackAnalysisService(text_generator=fake_text_generator)


@pytest.fixture
def sample_saved_track(
    saved_track_factory: ModelFactory[SavedTrack],
) -> SavedTrack:
    return saved_track_factory.build()


@pytest.fixture
def sample_lyrics() -> str:
    return "Test lyrics about love and loss"


@pytest.fixture
def simple_lyrics() -> str:
    return "Test lyrics"
