"""Domain models for library sync operations."""

from pydantic import BaseModel, Field

from .track import SavedTrack


class SyncProgress(BaseModel):
    """Progress update for library sync."""

    current: int
    total: int
    song_title: str
    artist_name: str


class EnrichedTrack(BaseModel):
    """Track enriched with lyrics and AI-generated vibe description."""

    track: SavedTrack
    lyrics: str
    vibe_description: str | None = Field(
        default=None,
        description="AI-generated vibe description",
    )

    @property
    def saved_track(self) -> SavedTrack:
        return self.track

    @property
    def track_id(self) -> str:
        return self.saved_track.track_id

    @property
    def has_lyrics(self) -> bool:
        return bool(self.lyrics)
