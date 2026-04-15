"""ChromaDB vector database repository."""

from typing import Optional

from chromadb import Collection, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pydantic import BaseModel

from vibra.domain import EnrichedTrack
from vibra.utils import LogLevel, Settings, log


class VectorDBRepository(BaseModel):
    """Repository for ChromaDB vector database operations."""

    _client: Optional[PersistentClient] = None  # noqa

    @property
    def client(self) -> PersistentClient:
        """Lazy-load persistent ChromaDB client."""
        if self._client is None:
            Settings.CHROMADB_PATH.mkdir(parents=True, exist_ok=True)
            log(
                f"Initializing ChromaDB client at {Settings.CHROMADB_PATH}",
                LogLevel.INFO,
            )
            self._client = PersistentClient(path=str(Settings.CHROMADB_PATH))
        return self._client

    @property
    def collection(self) -> Collection:
        return self.get_or_create_collection()

    def get_or_create_collection(self) -> Collection:
        """Get or create a collection by name with cosine similarity."""
        return self.client.get_or_create_collection(
            name=Settings.CHROMADB_COLLECTION,
            embedding_function=OllamaEmbeddingFunction(
                model_name=Settings.EMBEDDING_MODEL
            ),
            metadata={"hnsw:space": "cosine"},  # Use cosine similarity
        )

    def add_track(self, enriched_track: EnrichedTrack) -> None:
        """Add a single enriched track to the collection."""
        if not enriched_track.vibe_description:
            return

        track = enriched_track.track.track

        metadata = {
            "track_id": enriched_track.track_id,
            "track_name": track.name,
            "artist_names": track.artist_names,
            "album_name": track.album.name,
            "has_lyrics": enriched_track.has_lyrics,
            "genres": track.all_genre_names,
            "popularity": track.popularity,
            "spotify_url": track.spotify_url,
        }

        log(
            f"Storing track '{track.name}' with genres: '{track.all_genre_names}'",
            LogLevel.DEBUG,
        )

        self.collection.add(
            ids=[enriched_track.track_id],
            documents=[enriched_track.vibe_description],
            metadatas=[metadata],
        )

    def add_tracks(self, enriched_tracks: list[EnrichedTrack]) -> None:
        """Add multiple enriched tracks to the collection in a single batch."""
        valid_tracks = [t for t in enriched_tracks if t.vibe_description]
        if not valid_tracks:
            return

        log(f"Adding {len(valid_tracks)} tracks to VectorDB...", LogLevel.INFO)

        ids = []
        documents = []
        metadatas = []

        for enriched_track in valid_tracks:
            track = enriched_track.track.track
            ids.append(enriched_track.track_id)
            documents.append(enriched_track.vibe_description)
            metadatas.append({
                "track_id": enriched_track.track_id,
                "track_name": track.name,
                "artist_names": track.artist_names,
                "album_name": track.album.name,
                "has_lyrics": enriched_track.has_lyrics,
                "genres": track.all_genre_names,
                "popularity": track.popularity,
                "spotify_url": track.spotify_url,
            })

        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)
        log("Successfully added tracks to VectorDB.", LogLevel.INFO)

    def delete_tracks(self, track_ids: list[str]) -> None:
        log(f"Deleting {len(track_ids)} tracks from VectorDB...", LogLevel.INFO)
        self.collection.delete(ids=track_ids)

    def track_exists(self, track_id: str) -> bool:
        result = self.collection.get(ids=[track_id])
        return len(result["ids"]) > 0

    def search_by_vibe(self, query: str, n_results: int = 10) -> dict[str, list]:
        """Search for tracks by vibe description using semantic similarity."""
        log(f"Searching for vibe: '{query}'", LogLevel.INFO)
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
        )
        log(f"Found {len(results['ids'][0])} matching tracks", LogLevel.INFO)
        return results  # type: ignore[no-any-return]

    def get_all_tracks(self) -> dict[str, list]:
        log("Retrieving all tracks from VectorDB...", LogLevel.INFO)
        return self.collection.get()  # type: ignore[no-any-return]

    def count_tracks(self) -> int:
        return int(self.collection.count())
