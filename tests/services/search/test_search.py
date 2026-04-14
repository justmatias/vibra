import pytest

from vibra.domain import SearchResults
from vibra.services import SearchService


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.usefixtures("_populate_search_tracks")
async def test_search_by_vibe_returns_search_results_domain_model(
    search_service: SearchService,
    sample_query: str,
) -> None:
    result = await search_service.search_by_vibe(sample_query, n_results=10)

    assert isinstance(result, SearchResults)
    assert result.query == sample_query
    assert result.has_results


@pytest.mark.vcr
@pytest.mark.asyncio
@pytest.mark.usefixtures("_populate_search_tracks")
async def test_similarity_score_conversion_from_distance(
    search_service: SearchService,
) -> None:
    result = await search_service.search_by_vibe("test query", n_results=10)

    for search_result in result.results:
        assert 0.0 <= search_result.similarity_score <= 1.0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_empty_results_returns_valid_domain_model(
    search_service: SearchService,
) -> None:
    result = await search_service.search_by_vibe("nonexistent vibe", n_results=10)

    assert isinstance(result, SearchResults)
    assert result.total_results == 0
    assert not result.has_results
    assert result.query == "nonexistent vibe"
