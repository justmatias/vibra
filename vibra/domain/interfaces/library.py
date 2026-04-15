from typing import Protocol, runtime_checkable

from vibra.domain.track import SavedTrack, SpotifyArtist


@runtime_checkable
class Library(Protocol):
    """Protocol for a music library data source."""

    def get_all_liked_songs(self, max_tracks: int = 500) -> list[SavedTrack]: ...

    def get_artists(self, artist_ids: list[str]) -> list[SpotifyArtist]: ...
