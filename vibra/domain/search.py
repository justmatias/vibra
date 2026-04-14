from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    track_id: str
    track_name: str = Field(default="")
    artist_names: str = Field(default="")
    album_name: str = Field(default="")
    vibe_description: str
    distance: float = Field(ge=0.0, description="Distance from query (lower is better)")
    genres: str = Field(default="")
    popularity: int = Field(default=0)
    spotify_url: str = Field(default="")

    @property
    def similarity_score(self) -> float:
        """Similarity score computed from distance (0-1, higher is better)."""
        return 1 - self.distance


class SearchResults(BaseModel):
    query: str
    results: list[SearchResult] = Field(default_factory=list)
    total_results: int

    @property
    def has_results(self) -> bool:
        return self.total_results > 0
