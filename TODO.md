# TODO - Backend API for Next.js Frontend Integration

The Next.js frontend needs a REST/streaming API exposed by this service.
All endpoints below must be implemented before the Streamlit UI can be removed.

---

## 1. Add FastAPI (or similar) to the project

- Add `fastapi` and `uvicorn` to dependencies
- Add `poe api` command to `pyproject.toml` to start the API server
- Wire up the existing DI containers (`InfrastructureContainer`, `ServicesContainer`) into the FastAPI lifespan context

---

## 2. Auth endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/auth/authorize` | Return Spotify OAuth URL for the frontend to redirect to |
| `POST` | `/api/auth/callback` | Exchange Spotify `code` param for access token; return token to client |
| `POST` | `/api/auth/refresh` | Refresh an expired access token |
| `POST` | `/api/auth/logout` | Clear server-side cached token |
| `GET` | `/api/auth/me` | Return current user profile (`SpotifyUser`) |

Notes:
- Token caching strategy needs a decision: server-side (current, one user) vs. client-side JWT. Current cache file (`data/cache/.spotify_cache`) only supports a single user.
- CORS must allow the Next.js origin.

---

## 3. Search endpoint

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/search` | Semantic vibe search |

Request body:
```json
{ "query": "string", "n_results": 10 }
```

Response:
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
      "spotify_url": "string"
    }
  ]
}
```

Notes:
- `SearchService.search_by_vibe` is async - works directly with FastAPI.
- LLM query refinement is already handled inside the service.

---

## 4. Library sync endpoint (SSE stream)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/library/sync` | Start a sync; stream progress as Server-Sent Events |

Request body:
```json
{ "limit": 50 }
```

SSE event stream (two event types):

`progress` event:
```json
{ "type": "progress", "current": 5, "total": 50, "song_title": "...", "artist_name": "..." }
```

`track` event (on each completed enriched track):
```json
{ "type": "track", "track_id": "...", "track_name": "...", "artist_names": "...", "has_lyrics": true }
```

`done` event:
```json
{ "type": "done", "synced": 50, "with_lyrics": 42, "with_vibes": 42 }
```

Notes:
- `LibrarySyncService.sync_library` is a sync generator - wrap with `asyncio.to_thread` or convert to async generator for SSE.
- Access token must be passed per-request (header or body) so the Spotify client can be instantiated.

---

## 5. Library management endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/library/tracks` | Return all indexed tracks with metadata |
| `GET` | `/api/library/stats` | Return counts (total, with lyrics, with vibes) |
| `DELETE` | `/api/library` | Clear the entire ChromaDB collection |

---

## 6. Multi-user support (future / deferred)

Current architecture supports a single authenticated user (token cached to a single file).
If the Next.js app will serve multiple users:
- Replace file cache with a per-session or per-user token store (Redis, DB, or signed cookies)
- Update `SpotifyAuthManager` to accept a user identifier
- Update `SpotifyClient` factory to be keyed per user, not per process

---

## 7. Remove Streamlit UI

Once the API is complete and the Next.js frontend is functional:
- Remove `vibra/ui/` directory
- Remove `streamlit` and related UI packages from `pyproject.toml`
- Remove `poe dev` command (replace with `poe api`)
- Update `CLAUDE.md` and `README.md`
