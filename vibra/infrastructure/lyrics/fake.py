"""In-memory fake that satisfies the LyricsProvider protocol."""


class FakeLyricsProvider:
    """Lightweight test double for any LyricsProvider consumer."""

    def __init__(self, lyrics: str = "Fake song lyrics for testing purposes") -> None:
        self._lyrics = lyrics

    def search_song(self, title: str, artist: str) -> str:
        _title = title
        _artist = artist
        return self._lyrics
