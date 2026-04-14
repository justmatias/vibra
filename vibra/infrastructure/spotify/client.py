"""Spotify API client wrapper using spotipy."""

from functools import cached_property
from itertools import batched
from typing import Any

import stamina
from pydantic import BaseModel
from spotipy import Spotify

from vibra.domain import SavedTrack, SpotifyUser
from vibra.domain.track import SpotifyArtist
from vibra.utils.logger import LogLevel, log

from .config import RETRY_ON


class SpotifyClient(BaseModel):
    access_token: str

    @cached_property
    def client(self) -> Spotify:
        return Spotify(auth=self.access_token)

    @property
    def current_user(self) -> SpotifyUser:
        user_data = self._fetch_current_user()
        return SpotifyUser.from_api_response(user_data)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _fetch_current_user(self) -> dict[str, Any]:
        return self.client.current_user()  # type: ignore[no-any-return]

    @stamina.retry(on=RETRY_ON, attempts=3)
    def get_liked_songs(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        return self.client.current_user_saved_tracks(limit=limit, offset=offset)  # type: ignore[no-any-return]

    def get_all_liked_songs(self, max_tracks: int = 500) -> list[SavedTrack]:
        log(f"Fetching up to {max_tracks} liked songs...", LogLevel.INFO)

        all_tracks: list[SavedTrack] = []
        offset = 0

        while offset < max_tracks:
            items = self.get_liked_songs(limit=50, offset=offset).get("items", [])
            if not items:
                break  # pragma: no cover
            all_tracks.extend(SavedTrack.from_api_response(item) for item in items)
            offset += 50

        result = all_tracks[:max_tracks]
        log(f"Fetched {len(result)} liked songs.", LogLevel.INFO)
        return result

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _fetch_artists_batch(self, batch: list[str]) -> dict[str, Any]:
        return self.client.artists(batch)  # type: ignore[no-any-return]

    def get_artists(self, artist_ids: list[str]) -> list[SpotifyArtist]:
        unique_ids = sorted(set(artist_ids))
        all_artists: list[SpotifyArtist] = []

        log(f"Fetching {len(unique_ids)} unique artists...", LogLevel.INFO)

        for batch in batched(unique_ids, 50):
            response = self._fetch_artists_batch(list(batch))
            for artist in response.get("artists", []):
                if not artist:
                    continue  # pragma: no cover
                all_artists.append(SpotifyArtist.from_api_response(artist))

        log(f"Retrieved {len(all_artists)} artists.", LogLevel.INFO)
        return all_artists
