# 🎵 Project: Spotify Semantic Search (Deep Lyrics Edition)

## 📋 Overview

This project builds a semantic search engine for your Spotify "Liked Songs" library. It overcomes the deprecation of Spotify's Audio Features API and the lack of emotional context by combining three data sources:

1. **Spotify:** Base metadata (Title, Artist, Album).
2. **Genius:** Full song lyrics.
3. **LLM (AI):** Analyzes the cognitive dissonance between the musical genre and the lyrical meaning (e.g., "Happy sounding music with sad lyrics").

---

## 🛠 Tech Stack

### Core

- **Language:** Python 3.12+
- **Package Manager:** `uv`
- **Validation:** `Pydantic` (v2)
- **Dependency Injection:** `dependency-injector`

### AI & Vector Search

- **LLM:** `Ollama` (Llama 3.2 / Mistral) via OpenAI-compatible API
- **Embeddings:** `nomic-embed-text` (Ollama)
- **Vector Database:** `ChromaDB` (Local, persistent)
  - _Planned:_ Migration to `LightRAG` for graph-based knowledge representation

### Data Sources

- **Spotify:** `spotipy` (Spotify Web API)
- **Lyrics:** `lyricsgenius` (Genius API wrapper)

### Frontend

- **Framework:** `React` (separate repository)
- **API:** FastAPI backend (this repository)

### Development

- **Testing:** `pytest`, `pytest-vcr`, `polyfactory`
- **Linting:** `ruff`, `pylint`, `mypy`
- **Tasks:** `poethepoet`

---

## 📅 Implementation Phases

## Phase 1: Environment & Credentials

You now need keys for two different kingdoms.

1. **Spotify App:** Get your `CLIENT_ID` and `CLIENT_SECRET` from the Spotify Developer Dashboard.
2. **Genius API:**
   - Go to [Genius API Clients](https://genius.com/api-clients).
   - Create an app to generate your `GENIUS_ACCESS_TOKEN`.

3. **Environment Setup:**
   - Create a `.env` file:

   ```ini
   SPOTIPY_CLIENT_ID="..."
   SPOTIPY_CLIENT_SECRET="..."
   SPOTIPY_REDIRECT_URI="http://localhost:8501/"
   GENIUS_ACCESS_TOKEN="..."
   OPENAI_API_KEY="sk-..."
   ```

## Phase 2: Data Ingestion

This is where the slow magic happens. Downloading lyrics takes longer than fetching metadata.

1. **Fetch Spotify Data:**
   - Get the user's `Saved Tracks`.
   - Get the Artist's Genres (via Batch API call).

2. **Fetch Genius Data (New Step):**
   - Initialize: `genius = lyricsgenius.Genius(token)`.
   - **Search Strategy:** Iterate through the tracks.
   - _Sanitization:_ Clean the title before searching (remove "Remastered 2009", "- Live", etc.) to improve hit rate.
   - _Call:_ `song = genius.search_song(title, artist)`.
   - _Error Handling:_ If no lyrics are found or a timeout occurs, save `lyrics: "Not found/Instrumental"`.

## Phase 3: Deep Vibe Enrichment

The prompt is now much more sophisticated to leverage the textual data.

1. **Inference Logic:**
   - Function: `analyze_track_deeply(metadata, lyrics_text)`.
   - **Truncation:** Lyrics can be long. Truncate to the first 1000-1500 characters to save tokens; the chorus and main theme are usually found there.

2. **The Master Prompt:**

   > "Act as an expert music critic. Analyze this song:

   > - **Title:** {title}
   > - **Artist:** {artist}
   > - **Musical Genres:** {genres}
   > - **Lyrics Snippet:** "{lyrics_snippet}..."

   > **Task:**

   > 1. Detect the core theme of the lyrics (love, protest, grief, party).
   > 2. Contrast the lyrics with the musical genre (Is it a sad song with a happy rhythm?).
   > 3. Generate a synthetic **Vibe Description** for search purposes.

   > **Output:** Only the descriptive sentence."

3. **Result:** _"An Indie Pop track with an upbeat tempo, but the lyrics sarcastically address modern social isolation."_

## Phase 4: Vector Storage

Similar to the previous plan, but the embedding quality will be superior.

1. **Embed:** Use `text-embedding-3-small` on the generated description.
2. **Metadata:** Store `has_lyrics: bool` in ChromaDB so you can filter later if desired.

## Phase 5: Retrieval & Chat

The search flow remains, but the "DJ" response will be smarter.

1. **Query:** "I want songs that sound happy but are deep down sad."
2. **Match:** Thanks to the Phase 3 analysis, the system will find those songs with cognitive dissonance.
3. **Response:** The LLM can quote a line from the lyrics to justify its choice.

## Phase 6: API & Frontend Integration

Since Genius is slow, progress feedback through the API is critical.

1. **Real Progress via SSE or WebSocket:**
   - Expose a streaming endpoint so the React frontend can render a live progress bar.
   - Emit events per processed song (Spotify + Genius + LLM).

2. **Limit Control:**
   - Accept a `limit` query parameter (default 20, max 100) on the sync endpoint.

3. **Track Detail Endpoint:**
   - Return the AI vibe analysis alongside standard track metadata so the frontend can render it in an expandable card.

## 🚀 Definition of Done

1. **Login:** User logs in via Spotify.
2. **Config:** Select "Analyze last 10 songs".
3. **Wait:** User sees the progress bar advance while logs show _"Downloading lyrics for 'Bohemian Rhapsody'..."_.
4. **Chat:** User asks _"Which songs talk about making a mistake?"_.
5. **Result:** App returns specific songs based on lyrical content, not just the title.

---

## 🚀 Improvements & Feature Roadmap

### ✅ Completed Features

- [x] **Caching Strategy**: Implemented aggressive caching layer for Genius lyrics to reduce API hits on re-syncs.
- [x] **Incremental Sync**: Only analyze _newly added_ tracks instead of re-scanning the last N tracks every time.

---

## Phase 7: Code Quality Improvements 🔧

> **Goal:** Enhance the current implementation with better practices, performance, and maintainability.

### 7.1 Error Handling & Resilience

- [x] **Retry Logic with Exponential Backoff**: Add retry decorators to all API calls.
  - **Files:** `infrastructure/*/client.py`, `infrastructure/*/config.py`
  - **Implementation:** Used `stamina` library with `RETRY_ON` constants in config files.
  - **Clients updated:** `GeniusClient`, `LLMClient`, `SpotifyClient`, `SpotifyAuthManager`

- [x] **Graceful Degradation**: Continue sync even if individual track enrichment fails.
  - **Files:** `services/library_sync.py`
  - **Implementation:** Wrapped track enrichment in try/except, logs warning and continues.

### 7.2 Performance Optimizations

- [x] **Async Batching for LLM Inference**: Process multiple tracks concurrently for faster sync.
  - **Files:** `services/track_analysis.py`, `infrastructure/llm/client.py`
  - **Implementation:** Use `asyncio` with configurable concurrency limit (default 3).

- [x] **Batch Embedding Generation**: Generate embeddings in batches instead of one-by-one.
  - **Files:** `infrastructure/vectordb/repository.py`
  - **Current:** Uses Ollama's embedding function per-document.
  - **Improvement:** Batch up to 10 documents per embedding call.

- [x] **Connection Pooling**: Reuse HTTP connections for external APIs.
  - **Files:** `infrastructure/genius/client.py`, `infrastructure/llm/client.py`
  - **Implementation:** Use `httpx` with persistent sessions.

### 7.3 Search Experience Enhancements

- [ ] **Filters**: Add explicit filters for Genre, Year, or Popularity range to narrow down semantic search.
  - **Files:** `services/search.py`, `api/routers/search.py`
  - **Implementation:** Accept filter query params and apply metadata filters in ChromaDB query.

- [ ] **Audio Preview**: Return Spotify preview URL in search results for the React frontend to embed.
  - **Files:** `api/routers/search.py`, `domain/track.py`
  - **Implementation:** Include `preview_url` field in search result schema.

- [ ] **Playlist Creation**: Expose endpoint to create a Spotify playlist from a list of track IDs.
  - **Files:** `infrastructure/spotify/client.py`, `services/search.py`, `api/routers/playlists.py`
  - **Implementation:** Use Spotify API `user_playlist_add_tracks` endpoint.

### 7.4 API Improvements

- [ ] **Export Search Results**: Return results in JSON (default) with an optional `format=csv` query param.
  - **Files:** `api/routers/search.py`

---

## Phase 7.5: Operational Endpoints

These are small additions to the API that improve day-to-day usability and are prerequisites for the React frontend's first-load experience.

- [ ] **Health / status endpoint:** `GET /status` returns Ollama model availability, ChromaDB document count, and last sync timestamp. Frontend uses this to show app state before the user triggers a sync.
- [ ] **Re-sync trigger:** `POST /library/sync` accepts an optional `{ "limit": 20 }` body and returns a job ID. Progress is streamed via `GET /library/sync/{job_id}/stream` (SSE). This makes the incremental sync story explicit in the API.
- [ ] **Feedback endpoint:** `POST /tracks/{id}/feedback` with `{ "signal": "like" | "dislike" }`. Stores signal in ChromaDB metadata for future re-ranking (used by Phase 10).

---

## Phase 8: Friend Music Comparison 🆕

> **Goal:** Enable users to compare their music taste with friends by entering a Spotify username, computing overlap against the friend's public playlists, and surfacing cross-library recommendations.

**Note:** Spotify's API only exposes public playlists for other users - liked songs are private. Comparison is scoped to tracks the friend has made public.

### 8.1 Domain Model

#### [NEW] `domain/user_comparison.py`

```python
class UserProfile:
    spotify_id: str
    display_name: str
    track_ids: list[str]
    top_genres: list[str]
    top_artists: list[str]

class MusicSimilarity:
    user_a: str
    user_b: str
    overall_score: float  # 0-100%, Jaccard over track+artist+genre sets
    shared_tracks: list[str]
    shared_artists: list[str]
    shared_genres: list[str]
    recommendations: list[str]  # track IDs from B not in A's library
```

### 8.2 Infrastructure Changes

#### [MODIFY] `infrastructure/spotify/client.py`

```python
def get_user_playlists(self, user_id: str) -> list[dict]:
    return self.client.user_playlists(user_id)

def get_playlist_tracks(self, playlist_id: str) -> list[SavedTrack]:
    ...
```

### 8.3 Service Layer

#### [NEW] `services/user_comparison.py`

Similarity is computed as a weighted Jaccard score over shared tracks, artists, and genres - no graph DB needed. ChromaDB metadata already contains artist and genre fields.

```python
class UserComparisonService:
    spotify_client: SpotifyClient

    def fetch_friend_library(self, spotify_username: str) -> UserProfile:
        """Collect tracks from all of the friend's public playlists."""
        ...

    def calculate_similarity(
        self, current: UserProfile, friend: UserProfile
    ) -> MusicSimilarity:
        """Set intersection over tracks, artists, genres -> weighted score."""
        ...

    def recommend_from_friend(
        self, similarity: MusicSimilarity, n: int = 10
    ) -> list[str]:
        """Return tracks from friend's library not in current user's library,
        ranked by how well they match the current user's top genres."""
        ...
```

### 8.4 API Endpoints

#### [NEW] `api/routers/comparison.py`

```python
# POST /comparison
# Body: { "friend_username": "spotify_username" }
# Returns: MusicSimilarity

# GET /comparison/{friend_username}/recommendations
# Returns: list of track IDs from friend's library the current user may like
```

### 8.5 Data Flow

```
1. User enters friend's Spotify username
           ↓
2. SpotifyClient fetches friend's public playlists + tracks
           ↓
3. UserComparisonService computes set intersections
           ↓
4. Recommendations ranked by genre match against current user's library
           ↓
5. React frontend renders similarity scores + recommendation list
```

### 8.6 Tests

```bash
uv run pytest tests/services/user_comparison/ -v
```

**Test files to create:**

- `tests/services/user_comparison/test_user_comparison.py`
- `tests/domain/user_comparison/test_user_profile.py`

## Phase 9: Music DJ Agent 🤖

> **Goal:** Implement a conversational agent that can search, discover, and manage music through natural language.

**Implementation note:** Small local models (Llama 3.2) are unreliable at structured tool use. The LLM backend for the agent should be configurable - defaulting to a cloud provider (e.g. Claude) for reliable function calling, with local Ollama as a fallback for users who prefer it. The agent is implemented as intent classification + routing rather than a free-form ReAct loop, which is more robust with smaller models.

### 9.1 Agent Tools

```python
@tool
def search_library_by_vibe(query: str, n_results: int = 10) -> list[SearchResult]:
    """Search user's liked songs by vibe description."""
    ...

@tool
def discover_new_music(seed_query: str, n_results: int = 10) -> list[Track]:
    """Discover new music from Spotify based on vibe seeds."""
    ...

@tool
def create_playlist(name: str, track_ids: list[str]) -> str:
    """Create a Spotify playlist with given tracks."""
    ...

@tool
def get_track_analysis(track_id: str) -> str:
    """Get AI vibe description for a specific track."""
    ...

@tool
def compare_with_friend(friend_username: str) -> MusicSimilarity:
    """Compare music taste with a friend (Phase 8 integration)."""
    ...

@tool
def play_preview(track_id: str) -> str:
    """Get 30-second preview URL for a track."""
    ...
```

### 9.2 Conversation Flow

```
User: "I'm feeling nostalgic, find me something from the 90s"
        ↓
Agent: [Thought] User wants nostalgic 90s music from their library
       [Action] search_library_by_vibe("nostalgic 90s vibes")
       [Observation] Found 8 tracks matching the query
        ↓
Agent: "Found 8 nostalgic tracks from the 90s! Here are the top 3:
        1. 🎵 Wonderwall - Oasis
        2. 🎵 Creep - Radiohead
        3. 🎵 Losing My Religion - R.E.M.

        Want me to discover more like these or create a playlist?"
        ↓
User: "Yes, create a playlist called 'Rainy Day Nostalgia'"
        ↓
Agent: [Action] create_playlist("Rainy Day Nostalgia", [...track_ids])
       [Observation] Playlist created successfully
        ↓
Agent: "Done! Created 'Rainy Day Nostalgia' with 8 tracks.
        🔗 Open in Spotify: https://..."
```

### 9.3 Implementation Details

#### [NEW] `infrastructure/agent/tools.py`

Tool wrappers that delegate to existing services (`SearchService`, `LibrarySyncService`, `SpotifyClient`).

#### [NEW] `infrastructure/agent/agent.py`

```python
class MusicDJAgent:
    def __init__(self, llm_client: LLMClient, tools: list[Tool]):
        self.llm = llm_client
        self.tools = {t.name: t for t in tools}
        self.conversation_history: list[Message] = []

    def chat(self, user_message: str) -> AgentResponse:
        # 1. Classify intent (search / discover / create_playlist / preview / compare)
        # 2. Call the matching tool
        # 3. Format response with tracks
        ...
```

The LLM backend is injected - the same `LLMClient` abstraction used elsewhere, so swapping between Ollama and a cloud provider requires only config changes.

#### [NEW] `api/routers/agent.py`

```python
# POST /agent/chat
# Body: { "message": "I'm feeling nostalgic, find me something from the 90s" }
# Returns: { "response": "...", "tracks": [...] }
```

---

## Phase 10: Personalized Search Ranking 🧠

> **Goal:** Improve search relevance based on explicit user feedback without requiring model fine-tuning.

LoRA fine-tuning requires a GPU and significant user effort - not realistic for a local app. Feedback-based re-ranking achieves most of the personalization benefit with a fraction of the complexity.

### Features

- [ ] **Feedback endpoint:** `POST /tracks/{id}/feedback` with `{ "signal": "like" | "dislike" }`. Store signal as ChromaDB metadata.
- [ ] **Re-ranking:** After vector search, boost tracks with prior positive signals and bury those with negative ones before returning results.
- [ ] **Custom vibe labels:** User can tag a search result with a custom label (e.g. "coding music"). Labels stored in ChromaDB metadata and used as additional filter terms in future queries.
- [ ] **Feedback export:** `GET /feedback/export` returns all signals as JSON for inspection or backup.

---

## Phase 11: Voice & Multi-Modal Input 🎙️

> **Goal:** Enable natural voice commands and image-based music discovery.

### 11.1 Voice Search

- [ ] Integrate Whisper (local) for speech-to-text
- [ ] Voice command: "Hey DJ, play something for a rainy Sunday"
- [ ] Voice feedback: "Not this vibe, something more upbeat"

### 11.2 Multi-Modal Input

- [ ] Accept image uploads (sunset photo, party scene, etc.)
- [ ] Use vision model (LLaVA/GPT-4V) to describe image mood
- [ ] Convert visual vibe to music search query
- [ ] Example: Upload beach sunset → "Chill, warm, nostalgic summer vibes"

---

## Phase 12: Social Features 🌐

> **Goal:** Make music discovery a social experience.

**Note:** Leaderboards, shareable cards, and hosted compatibility scores require a shared backend, which conflicts with the local, privacy-first architecture. Features below are scoped to what can be done without a central server.

### Features

- [ ] **Group Playlists**: Given multiple friends' usernames, compute the intersection of their public playlists and create a Spotify playlist from the overlap + genre-balanced exploration tracks.
  - Input: list of Spotify usernames
  - Output: playlist optimized for shared taste + discovery
- [ ] **Export Comparison Card**: Generate a self-contained HTML/PNG card from a `MusicSimilarity` result that the user can share manually (no upload required).
