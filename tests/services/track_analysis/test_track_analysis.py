import pytest

from vibra.domain import SavedTrack
from vibra.services import TrackAnalysisService


@pytest.mark.vcr
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
    # Verify the vibe description is meaningful (should be at least a sentence)
    # The prompt asks for 2-3 sentences, so we expect at least 50 characters
    assert len(result) > 50, "Vibe description should be a meaningful sentence"


@pytest.mark.vcr
def test_analyze_track_builds_correct_prompt(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
) -> None:
    prompt = track_analysis_service._build_analysis_prompt(  # pylint: disable=protected-access
        sample_saved_track, simple_lyrics
    )

    # Verify the prompt contains key information
    assert sample_saved_track.track.name in prompt
    assert sample_saved_track.track.album.name in prompt
    assert simple_lyrics in prompt
    assert "Vibe Description" in prompt


@pytest.mark.usefixtures("mock_llm_exception")
@pytest.mark.asyncio
async def test_analyze_track_handles_exceptions(
    track_analysis_service: TrackAnalysisService,
    sample_saved_track: SavedTrack,
    simple_lyrics: str,
) -> None:
    result = await track_analysis_service.analyze_track(
        sample_saved_track, simple_lyrics
    )

    assert result is None
