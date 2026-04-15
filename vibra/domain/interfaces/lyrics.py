from typing import Protocol, runtime_checkable


@runtime_checkable
class LyricsProvider(Protocol):
    """Protocol for fetching song lyrics."""

    def search_song(self, title: str, artist: str) -> str: ...
