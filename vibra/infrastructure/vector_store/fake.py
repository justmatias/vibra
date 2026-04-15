"""In-memory fake that satisfies the VectorStore protocol."""

from vibra.domain.sync import EnrichedTrack


class FakeVectorStore:
    """Lightweight test double for any VectorStore consumer."""

    def __init__(self) -> None:
        self._tracks: dict[str, EnrichedTrack] = {}

    def add_track(self, enriched_track: EnrichedTrack) -> None:
        if enriched_track.vibe_description:
            self._tracks[enriched_track.track_id] = enriched_track

    def add_tracks(self, enriched_tracks: list[EnrichedTrack]) -> None:
        for track in enriched_tracks:
            self.add_track(track)

    def delete_tracks(self, track_ids: list[str]) -> None:
        for track_id in track_ids:
            self._tracks.pop(track_id, None)

    def track_exists(self, track_id: str) -> bool:
        return track_id in self._tracks

    def search_by_vibe(self, query: str, n_results: int = 10) -> dict[str, list]:  # pylint: disable=no-self-use
        _query = query
        tracks = list(self._tracks.values())[:n_results]
        return {
            "ids": [[t.track_id for t in tracks]],
            "documents": [[t.vibe_description for t in tracks]],
            "metadatas": [[self._to_metadata(t) for t in tracks]],
            "distances": [[0.1 * i for i in range(len(tracks))]],
        }

    def get_all_tracks(self) -> dict[str, list]:
        tracks = list(self._tracks.values())
        return {
            "ids": [t.track_id for t in tracks],
            "documents": [t.vibe_description for t in tracks],
            "metadatas": [self._to_metadata(t) for t in tracks],
        }

    def count_tracks(self) -> int:
        return len(self._tracks)

    def _to_metadata(self, track: EnrichedTrack) -> dict:  # pylint: disable=no-self-use
        spotify_track = track.track.track
        return {
            "track_id": track.track_id,
            "track_name": spotify_track.name,
            "artist_names": spotify_track.artist_names,
            "album_name": spotify_track.album.name,
            "has_lyrics": track.has_lyrics,
            "genres": spotify_track.all_genre_names,
            "popularity": spotify_track.popularity,
            "spotify_url": spotify_track.spotify_url,
        }
