import contextlib

from pydantic import BaseModel

from vibra.domain import SavedTrack
from vibra.infrastructure import LLMClient
from vibra.utils import LogLevel, log


class TrackAnalysisService(BaseModel):
    llm_client: LLMClient

    def _build_analysis_prompt(self, saved_track: SavedTrack, lyrics: str) -> str:  # pylint: disable=no-self-use
        genres = []
        for artist in saved_track.track.artists:
            genres.extend(artist.genres)

        return f"""
        Act as an expert music critic. Analyze this song:
            - **Title:** {saved_track.track.name}
            - **Artist:** {saved_track.track.artist_names}
            - **Album:** {saved_track.track.album.name}
            - **Musical Genres:** {", ".join(genres)}
            - **Popularity:** {saved_track.track.popularity}/100
            - **Lyrics Snippet:** "{lyrics}"

            **Task:**
            1. Detect the core theme of the lyrics (love, protest, grief, party, nostalgia, etc.)
            2. Analyze the emotional tone and mood of the lyrics
            3. Consider how the genre and artist style might contrast or align with the lyrical content
            4. Generate a synthetic **Vibe Description** for semantic search purposes

            **Output:** Only the descriptive sentence (max 2-3 sentences). Focus on the emotional essence and searchable characteristics.

            **Example:** "An indie folk track with melancholic lyrics about lost love and regret, delivered through poetic storytelling that evokes deep nostalgia and bittersweet reflection."

            Vibe Description:
        """

    async def analyze_track(self, saved_track: SavedTrack, lyrics: str) -> str | None:
        with contextlib.suppress(Exception):
            prompt = self._build_analysis_prompt(saved_track, lyrics)
            log(f"Prompt: {prompt}", LogLevel.DEBUG)
            vibe_description = await self.llm_client.generate(prompt)
            log(
                f"Generated vibe description for: {saved_track.track.name}",
                LogLevel.INFO,
            )
            return vibe_description
        log(
            f"Failed to generate vibe description for: {saved_track.track.name}",
            LogLevel.WARNING,
        )
        return None
