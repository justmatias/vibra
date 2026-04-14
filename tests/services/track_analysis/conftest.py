from collections.abc import Generator
from unittest.mock import patch

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import SavedTrack
from vibra.injections import container
from vibra.services import TrackAnalysisService


@pytest.fixture
def track_analysis_service() -> TrackAnalysisService:
    return container.services.track_analysis_service()  # type: ignore[no-any-return]


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


@pytest.fixture(
    params=[
        (RuntimeError, "LLM service unavailable"),
        (ValueError, "Invalid input"),
        (ConnectionError, "Network error"),
    ],
    ids=["RuntimeError", "ValueError", "ConnectionError"],
)
def mock_llm_exception(
    request: pytest.FixtureRequest,
) -> Generator[tuple[type[Exception], str], None, None]:
    """Fixture that mocks LLM client to raise various exceptions."""
    exception_class, error_message = request.param
    with patch(
        "vibra.infrastructure.llm.client.LLMClient.generate",
        side_effect=exception_class(error_message),
    ):
        yield exception_class, error_message
