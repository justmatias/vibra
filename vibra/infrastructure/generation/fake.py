"""In-memory fake that satisfies the TextGenerator protocol."""

DEFAULT_RESPONSE = (
    "A melancholic indie track with introspective lyrics about lost love "
    "and bittersweet nostalgia, wrapped in gentle acoustic arrangements."
)


class FakeTextGenerator:
    """Lightweight test double for any TextGenerator consumer."""

    def __init__(
        self,
        response: str = DEFAULT_RESPONSE,
        exception: type[Exception] | None = None,
        exception_message: str = "",
    ) -> None:
        self._response = response
        self._exception = exception
        self._exception_message = exception_message
        self.calls: list[str] = []

    async def generate(self, prompt: str) -> str:
        self.calls.append(prompt)
        if self._exception is not None:
            raise self._exception(self._exception_message)
        return self._response
