"""Library sync service for fetching and enriching Spotify tracks."""

import asyncio
from collections.abc import Generator

from pydantic import BaseModel, ConfigDict

from vibra.domain import EnrichedTrack, SavedTrack, SyncProgress
from vibra.domain.interfaces import Library, LyricsProvider, VectorStore
from vibra.utils.logger import LogLevel, log

from .track_analysis import TrackAnalysisService


class LibrarySyncService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    library: Library
    lyrics_provider: LyricsProvider
    track_analysis_service: TrackAnalysisService
    vector_store: VectorStore

    def sync_library(
        self, limit: int = 20
    ) -> Generator[SyncProgress | EnrichedTrack, None, None]:
        log(f"Starting library sync (limit={limit})...", LogLevel.INFO)

        saved_tracks = self.library.get_all_liked_songs(max_tracks=limit)
        self._enrich_artist_genres(saved_tracks)
        total = len(saved_tracks)
        log(f"Found {total} tracks to process.", LogLevel.INFO)

        for index, saved_track in enumerate(saved_tracks, start=1):
            yield SyncProgress(
                current=index,
                total=total,
                song_title=saved_track.track.name,
                artist_name=saved_track.track.artist_names,
            )
            yield from self._process_track(saved_track)

        log("Library sync completed.", LogLevel.INFO)

    def _process_track(
        self, saved_track: SavedTrack
    ) -> Generator[EnrichedTrack, None, None]:
        track = saved_track.track
        if self.vector_store.track_exists(track.id_):
            log(f"Skipping '{track.name}' - already indexed.", LogLevel.DEBUG)
            return

        try:
            enriched = self._enrich_track(saved_track)
            if enriched.vibe_description:
                self.vector_store.add_track(enriched)
            yield enriched
        except Exception as e:  # pragma: no cover  # noqa: BLE001
            log(f"Failed to enrich '{track.name}': {e}", LogLevel.WARNING)

    def _enrich_track(self, saved_track: SavedTrack) -> EnrichedTrack:
        """Enrich a track with lyrics and vibe description."""
        lyrics = self.lyrics_provider.search_song(
            title=saved_track.track.name,
            artist=saved_track.track.artist_names,
        )
        vibe_description = None

        if lyrics:
            vibe_description = asyncio.run(
                self.track_analysis_service.analyze_track(
                    saved_track=saved_track,
                    lyrics=lyrics,
                )
            )

        return EnrichedTrack(
            track=saved_track,
            lyrics=lyrics,
            vibe_description=vibe_description,
        )

    def _enrich_artist_genres(self, saved_tracks: list[SavedTrack]) -> None:
        """Enrich artist data with genres by fetching full artist details"""
        artist_ids = [
            artist.id_
            for saved_track in saved_tracks
            for artist in saved_track.track.artists
        ]
        artists_with_genres = self.library.get_artists(artist_ids)
        artist_map = {artist.id_: artist for artist in artists_with_genres}

        for saved_track in saved_tracks:
            saved_track.track.artists = [
                artist_map.get(artist.id_, artist)
                for artist in saved_track.track.artists
            ]

        log(
            f"Enriched {len(artists_with_genres)} artists with genre data.",
            LogLevel.INFO,
        )
