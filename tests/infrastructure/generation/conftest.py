# pylint: disable=protected-access
from unittest.mock import MagicMock

import pytest

from vibra.infrastructure import LLMClient


@pytest.fixture
def llm_client() -> LLMClient:
    return LLMClient()


@pytest.fixture
def llm_client_with_api_error() -> LLMClient:
    llm_client = LLMClient()

    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    llm_client.__dict__["client"] = mock_client

    return llm_client


@pytest.fixture
def simple_prompt() -> str:
    return "What is the capital of France? Answer in one word."


@pytest.fixture
def analysis_prompt() -> str:
    return """Analyze this song in one sentence:
    - Title: Bohemian Rhapsody
    - Artist: Queen
    - Genre: Rock
    - Theme: Complex narrative about a young man's existential crisis

    Provide a brief vibe description."""
