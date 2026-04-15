# TODO - Vibra Implementation Tasks

---

## Phase 1-3: Foundation (complete)

- [x] FastAPI + uvicorn wired up with DI containers
- [x] Auth endpoints: authorize, callback, refresh, logout, me
- [x] Infrastructure refactor to feature-based layout with protocols and fakes
- [x] Streamlit UI removed

---

## Phase 4: Core API Endpoints

### Search

- [ ] `POST /api/search` — semantic vibe search
  - Files: `api/routers/search.py`, `api/schemas/search.py`
  - `SearchService.search_by_vibe` is async, works directly with FastAPI
  - `preview_url` exists on `SpotifyTrack` but is not stored in ChromaDB metadata yet:
    1. Add `preview_url` to metadata dict in `VectorDBRepository.add_track` / `add_tracks` (`infrastructure/vector_store/repository.py:51`)
    2. Add `preview_url` field to `SearchResult` (`domain/search.py`)
    3. Pass it through in `SearchService._create_search_result` (`services/search.py:77`)

**Request:**
```json
{ "query": "string", "n_results": 10 }
```

**Response:**
```json
{
  "query": "string",
  "results": [
    {
      "track_id": "string",
      "track_name": "string",
      "artist_names": "string",
      "album_name": "string",
      "vibe_description": "string",
      "similarity_score": 0.0,
      "genres": "string",
      "popularity": 0,
      "spotify_url": "string",
      "preview_url": "string"
    }
  ]
}
```

- [ ] Add optional filters to `POST /api/search`: `genre`, `year_min`, `year_max`, `popularity_min`
  - Files: `services/search.py`, `api/routers/search.py`
  - Apply as ChromaDB metadata filters before vector search

- [ ] Add optional `?format=csv` query param to return search results as CSV
  - Files: `api/routers/search.py`

### Library Sync (SSE)

- [ ] `POST /api/library/sync` — start a sync; stream progress as Server-Sent Events
  - Files: `api/routers/library.py`
  - `LibrarySyncService.sync_library` is a sync generator — wrap with `asyncio.to_thread` or convert to async generator
  - Access token passed as `Authorization: Bearer <token>` header

**Request:**
```json
{ "limit": 50 }
```

**SSE event types:**

`progress`:
```json
{ "type": "progress", "current": 5, "total": 50, "song_title": "...", "artist_name": "..." }
```

`track`:
```json
{ "type": "track", "track_id": "...", "track_name": "...", "artist_names": "...", "has_lyrics": true }
```

`done`:
```json
{ "type": "done", "synced": 50, "with_lyrics": 42, "with_vibes": 42 }
```

### Library Management

- [ ] `GET /api/library/tracks` — return all indexed tracks with metadata
  - Files: `api/routers/library.py`
- [ ] `GET /api/library/stats` — return counts (total, with_lyrics, with_vibes, last_synced)
  - Files: `api/routers/library.py`
- [ ] `DELETE /api/library` — clear the entire ChromaDB collection
  - Files: `api/routers/library.py`

### Operational

- [ ] `GET /api/status` — app health for the React frontend first-load screen
  - Files: `api/routers/status.py`
  - Returns Ollama model availability, ChromaDB document count, last sync timestamp

**Response:**
```json
{
  "ollama_available": true,
  "models_loaded": ["llama3.2", "nomic-embed-text"],
  "track_count": 142,
  "last_synced": "2026-04-15T10:00:00Z"
}
```

### Playlists

- [ ] `POST /api/playlists` — create a Spotify playlist from a list of track IDs
  - Files: `infrastructure/library/client.py`, `api/routers/playlists.py`
  - Use Spotify API `user_playlist_add_tracks`

**Request:**
```json
{ "name": "string", "track_ids": ["string"] }
```

**Response:**
```json
{ "playlist_id": "string", "spotify_url": "string" }
```

---

## Phase 7: Multi-user Support

Current architecture supports a single authenticated user (token cached to `data/cache/.spotify_cache`). This must be resolved before friend comparison and any multi-tenant use of the API.

- [ ] Replace file cache with per-session token store (Redis or signed cookies)
- [ ] Update `SpotifyAuthManager` to accept a user identifier
- [ ] Update `SpotifyClient` factory to be keyed per user, not per process

---

## Phase 8: Friend Music Comparison

**Constraint:** Spotify API only exposes a user's *public playlists*, not their liked songs.

### Domain

- [ ] Create `vibra/domain/user_comparison.py`
  - `UserProfile`: spotify_id, display_name, track_ids, top_genres, top_artists
  - `MusicSimilarity`: user_a, user_b, overall_score (Jaccard), shared_tracks, shared_artists, shared_genres, recommendations

### Infrastructure

- [ ] Add `get_user_playlists(user_id: str) -> list[dict]` to `SpotifyClient`
- [ ] Add `get_playlist_tracks(playlist_id: str) -> list[SavedTrack]` to `SpotifyClient`
- [ ] Add corresponding methods to `Library` protocol and `FakeLibrary`

### Service

- [ ] Create `vibra/services/user_comparison.py` — `UserComparisonService`
  - `fetch_friend_library(spotify_username)` — collect tracks from all public playlists
  - `calculate_similarity(current, friend)` — weighted Jaccard over tracks, artists, genres
  - `recommend_from_friend(similarity, n=10)` — tracks from friend not in current user's library, ranked by genre match

### API

- [ ] `POST /api/comparison` — compute similarity with a friend
  - Body: `{ "friend_username": "string" }`
  - Returns: `MusicSimilarity`
- [ ] `GET /api/comparison/{friend_username}/recommendations` — tracks from friend's library the user may like

### Tests

- [ ] `tests/domain/user_comparison/test_user_profile.py`
- [ ] `tests/services/user_comparison/test_user_comparison.py`

---

## Phase 9: Music DJ Agent

**Note:** LLM backend must be configurable (cloud provider for reliable tool use, Ollama as fallback). Agent uses intent classification + routing, not a free-form ReAct loop.

### Infrastructure

- [ ] Create `vibra/infrastructure/agent/tools.py`
  - Tool wrappers delegating to `SearchService`, `SpotifyClient`, and `UserComparisonService`
  - Tools: `search_library_by_vibe`, `create_playlist`, `get_track_analysis`, `compare_with_friend`, `get_preview_url`
- [ ] Create `vibra/infrastructure/agent/agent.py` — `MusicDJAgent`
  - Intent classification: search / create_playlist / preview / compare
  - LLM backend injected via existing `TextGenerator` protocol

### DI

- [ ] Wire `MusicDJAgent` into `ServicesContainer`

### API

- [ ] `POST /api/agent/chat`
  - Body: `{ "message": "string", "history": [...] }`
  - Returns: `{ "response": "string", "tracks": [...], "intent": "string" }`

### Tests

- [ ] `tests/infrastructure/agent/test_agent.py` — intent classification with fake LLM
- [ ] `tests/api/routers/test_agent.py`

---

## Phase 10: Personalized Search Ranking

### Feedback Collection

- [ ] `POST /api/tracks/{track_id}/feedback`
  - Body: `{ "signal": "like" | "dislike" }`
  - Store signal as ChromaDB metadata field on the track document
- [ ] `GET /api/feedback/export` — return all stored signals as JSON

### Re-ranking

- [ ] Update `SearchService.search_by_vibe` to re-rank results after vector search
  - Boost tracks with prior `like` signals
  - Demote tracks with prior `dislike` signals
  - Files: `services/search.py`

### Custom Labels

- [ ] `POST /api/tracks/{track_id}/labels`
  - Body: `{ "label": "coding music" }`
  - Store label in ChromaDB metadata; use as additional filter term in future queries
- [ ] Update search to accept `?labels=coding+music` filter

### Tests

- [ ] `tests/services/search/test_search_reranking.py`

---

## Phase 11: Voice & Multi-Modal Input

### Voice Search

- [ ] Add `openai-whisper` (local) to dependencies
- [ ] Create `vibra/infrastructure/transcription/client.py` — `WhisperClient`
  - `transcribe(audio_bytes) -> str`
- [ ] Add `Transcription` protocol to `vibra/domain/interfaces/`
- [ ] `POST /api/search/voice`
  - Accepts audio file upload (wav/mp3/webm)
  - Transcribes with Whisper, then passes text to `SearchService.search_by_vibe`
  - Returns same schema as `POST /api/search`

### Image-to-Vibe Search

- [ ] Add vision model support to `TextGenerator` (LLaVA via Ollama)
- [ ] `POST /api/search/image`
  - Accepts image upload
  - Vision model generates a mood/vibe description from the image
  - Passes description to `SearchService.search_by_vibe`
  - Returns same schema as `POST /api/search`

### Tests

- [ ] `tests/infrastructure/transcription/test_whisper_client.py`
- [ ] `tests/api/routers/test_search_voice.py`

---

## Phase 12: Social Features

**Constraint:** All features must work without a central server (local only).

### Group Playlists

- [ ] `POST /api/playlists/group`
  - Body: `{ "friend_usernames": ["string"], "name": "string" }`
  - Fetch public playlists for each username via `SpotifyClient`
  - Compute intersection of tracks/genres across all users
  - Fill remaining slots with genre-balanced tracks from each user's library
  - Create and return a Spotify playlist

### Comparison Card Export

- [ ] `GET /api/comparison/{friend_username}/card`
  - Generates a self-contained HTML or PNG comparison card from a `MusicSimilarity` result
  - No external upload — user downloads and shares manually

