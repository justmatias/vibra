import asyncio

from pydantic import BaseModel, ConfigDict

from vibra.domain import SearchResult, SearchResults
from vibra.domain.interfaces import TextGenerator, VectorStore
from vibra.utils import LogLevel, log


class SearchService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    vector_store: VectorStore
    text_generator: TextGenerator

    async def search_by_vibe(self, query: str, n_results: int = 10) -> SearchResults:
        log(f"Searching for vibe: '{query}' (max {n_results} results)", LogLevel.INFO)

        refined_query = await self._refine_query(query)
        log(f"Refined query: '{refined_query}'", LogLevel.INFO)

        raw_results = await asyncio.to_thread(
            self.vector_store.search_by_vibe, refined_query, n_results
        )
        search_results = self._transform_results(query, raw_results)

        log(
            f"Found {search_results.total_results} matching tracks",
            LogLevel.INFO,
        )

        return search_results

    async def _refine_query(self, query: str) -> str:
        """Refine the user query to be more descriptive for semantic search."""
        prompt = (
            "You are an expert music curator. Rewrite the following search query to be "
            "more descriptive, capturing the mood, musical style, and lyrical themes "
            "implied by the user. This description will be used for semantic search "
            "against a database of song analyses. Return ONLY the refined query text.\n\n"
            f"Original query: '{query}'"
        )
        return await self.text_generator.generate(prompt)

    def _transform_results(
        self, query: str, raw_results: dict[str, list]
    ) -> SearchResults:
        # ChromaDB returns nested lists, we need the first element
        ids = raw_results.get("ids", [[]])[0]
        documents = raw_results.get("documents", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        results = [
            self._create_search_result(
                track_id=ids[i],
                vibe_description=documents[i],
                metadata=metadatas[i],
                distance=distances[i],
            )
            for i in range(len(ids))
        ]

        return SearchResults(
            query=query,
            results=results,
            total_results=len(results),
        )

    def _create_search_result(  # pylint: disable=no-self-use
        self,
        track_id: str,
        vibe_description: str,
        metadata: dict,
        distance: float,
    ) -> SearchResult:
        return SearchResult.model_validate({
            "track_id": track_id,
            "track_name": metadata.get("track_name"),
            "artist_names": metadata.get("artist_names"),
            "album_name": metadata.get("album_name"),
            "vibe_description": vibe_description,
            "distance": distance,
            "genres": metadata.get("genres"),
            "popularity": metadata.get("popularity"),
            "spotify_url": metadata.get("spotify_url"),
        })
