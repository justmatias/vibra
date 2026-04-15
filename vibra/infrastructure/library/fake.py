"""In-memory fake that satisfies the Library protocol."""

from vibra.domain.track import SavedTrack, SpotifyArtist


class FakeLibrary:
    """Lightweight test double for any Library consumer."""

    def __init__(self, liked_songs: list[SavedTrack] | None = None) -> None:
        self._liked_songs = liked_songs or []
        self.get_all_liked_songs_calls: list[dict] = []

    def get_all_liked_songs(self, max_tracks: int = 500) -> list[SavedTrack]:
        self.get_all_liked_songs_calls.append({"max_tracks": max_tracks})
        return self._liked_songs[:max_tracks]

    def get_artists(self, artist_ids: list[str]) -> list[SpotifyArtist]:
        seen: dict[str, SpotifyArtist] = {}
        for track in self._liked_songs:
            for artist in track.track.artists:
                if artist.id_ in artist_ids and artist.id_ not in seen:
                    seen[artist.id_] = artist
        return list(seen.values())
