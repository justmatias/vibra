# pylint: disable=protected-access
import pytest

from vibra.infrastructure import LLMClient


def test_client_reuses_instance(llm_client: LLMClient) -> None:
    client1 = llm_client.client
    client2 = llm_client.client
    assert client1 is client2


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_generate_simple_prompt(
    llm_client: LLMClient, simple_prompt: str
) -> None:
    response = await llm_client.generate(simple_prompt)
    assert isinstance(response, str)
    assert response == "Paris."


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_generate_analysis_prompt(
    llm_client: LLMClient, analysis_prompt: str
) -> None:
    response = await llm_client.generate(analysis_prompt)

    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_generate_returns_stripped_content(llm_client: LLMClient) -> None:
    response = await llm_client.generate("Say hello")
    assert not response.startswith(" ")
    assert not response.endswith(" ")


@pytest.mark.asyncio
async def test_generate_handles_api_error(llm_client_with_api_error: LLMClient) -> None:
    """Test that generate properly wraps API errors."""
    with pytest.raises(RuntimeError, match="Failed to generate text"):
        await llm_client_with_api_error.generate("test prompt")
