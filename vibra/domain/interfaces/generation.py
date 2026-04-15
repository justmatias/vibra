from typing import Protocol, runtime_checkable


@runtime_checkable
class TextGenerator(Protocol):
    """Protocol for LLM-based text generation."""

    async def generate(self, prompt: str) -> str: ...
