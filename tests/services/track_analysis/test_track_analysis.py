import pytest

from vibra.domain import SavedTrack
from vibra.infrastructure.generation.fake import FakeTextGenerator
from vibra.services import TrackAnalysisService


@pytest.mark.asyncio
async def test_analyze_track_success(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    sample_lyrics: str,
) -> None:
    result = await track_analysis_service.analyze_track(
        sample_saved_track, sample_lyrics
    )

    assert result
    assert isinstance(result, str)
    assert len(result) > 50, "Vibe description should be a meaningful sentence"


def test_analyze_track_builds_correct_prompt(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
) -> None:
    prompt = track_analysis_service._build_analysis_prompt(  # pylint: disable=protected-access
        sample_saved_track, simple_lyrics
    )

    assert sample_saved_track.track.name in prompt
    assert sample_saved_track.track.album.name in prompt
    assert simple_lyrics in prompt
    assert "Vibe Description" in prompt


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception_class,error_message",
    [
        (RuntimeError, "LLM service unavailable"),
        (ValueError, "Invalid input"),
        (ConnectionError, "Network error"),
    ],
    ids=["RuntimeError", "ValueError", "ConnectionError"],
)
async def test_analyze_track_handles_exceptions(
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
    exception_class: type[Exception],
    error_message: str,
) -> None:
    service = TrackAnalysisService(
        text_generator=FakeTextGenerator(
            exception=exception_class, exception_message=error_message
        )
    )
    result = await service.analyze_track(sample_saved_track, simple_lyrics)

    assert result is None
