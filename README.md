# 🎵 Vibra

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)
![ChromaDB](https://img.shields.io/badge/Vector-ChromaDB-green)
![Spotify API](https://img.shields.io/badge/Data-Spotify-1DB954)
![Genius](https://img.shields.io/badge/Lyrics-Genius-FFFF00)

A **LLM-powered search engine** application that lets you search your Spotify "Liked Songs" library using natural language descriptions of vibes and emotions.

> **Stop searching by Genre. Start searching by _Vibe_ and _Meaning_.** > **100% Local & Private.**
<img width="1582" height="813" alt="Screenshot from 2026-01-03 09-49-37" src="https://github.com/user-attachments/assets/e88b6c04-8a76-4fe8-a97a-0cc42bf5a134" />

## ✨ Features

- 🎭 **AI-Powered Vibe Analysis**: Uses local LLM to generate semantic descriptions of your music
- 🔍 **Natural Language Search**: Find songs by describing the vibe you want
- 🎨 **Beautiful Streamlit UI**: Modern, responsive interface for browsing and searching
- 🔒 **100% Local & Private**: All AI processing happens on your machine
- 📊 **Rich Track Metadata**: View popularity, genres, and Spotify links
- 🎯 **Similarity Scores**: See how well each track matches your query

<img width="1889" height="869" alt="Screenshot from 2026-02-21 14-11-30" src="https://github.com/user-attachments/assets/59b8c2f1-792b-4ec9-8cd6-4b74462ac06e" />
<img width="1889" height="869" alt="Screenshot from 2026-02-21 14-12-49" src="https://github.com/user-attachments/assets/b738708c-9adc-4db2-b9e3-db5ea70d13c2" />

## 🧠 How it Works

1. **Sync Your Library**

   - Fetches your liked songs from Spotify
   - Retrieves lyrics from Genius
   - Analyzes each track with a local LLM to generate vibe descriptions

2. **AI Analysis**

   - Combines audio features (energy, valence, tempo) with lyrical content
   - Generates rich, semantic descriptions like:
     - _"An upbeat indie track with melancholic lyrics about lost love and nostalgia"_
     - _"High-energy dance anthem with empowering lyrics about self-confidence"_

3. **Semantic Search**
   - Stores vibe descriptions as embeddings in ChromaDB
   - Search using natural language: _"sad songs about heartbreak"_
   - Returns tracks ranked by semantic similarity

## 🛠️ Tech Stack

### Backend

- **Language**: Python 3.12+
- **Framework**: Pydantic for data validation
- **Dependency Injection**: dependency-injector
- **Testing**: pytest

### Data Sources

- **Spotify Web API**: Track metadata and audio features
- **Genius API**: Song lyrics

### AI & Vector Search

- **LLM**: Ollama (Llama 3.2 / Mistral)
- **Embeddings**: Ollama nomic-embed-text
- **Vector DB**: ChromaDB (local persistence)

### UI

- **Framework**: Streamlit
- **Styling**: Custom CSS
- **Components**: Modular, reusable UI components

## 🚀 Quick Start

### Prerequisites

1. **Spotify App**

   - Create an app at [Spotify Dashboard](https://developer.spotify.com/dashboard)
   - Get your `CLIENT_ID` and `CLIENT_SECRET`

2. **Genius API**

   - Get a token from [Genius API Clients](https://genius.com/api-clients)

3. **Ollama**

   ```bash
   # Install Ollama
   curl -fsSL https://ollama.com/install.sh | sh

   # Pull required models
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/justmatias/vibra.git
   cd vibra
   ```

2. **Set up environment**

   ```bash
   # Copy environment template
   cp .env.sample .env

   # Edit .env with your credentials
   ```

3. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync
   ```

### Running the App

```bash
uv run poe dev
```

Navigate to `http://localhost:8501` in your browser.

## 📖 Usage

### 1. Connect to Spotify

- Click "Connect with Spotify" on the home page
- Authorize the application

### 2. Sync Your Library

- Choose how many songs to analyze (5-100)
- Click "Sync Library"
- Wait for the AI to analyze each track (2-3 seconds per song)

### 3. Search by Vibe

- Click "Search Vibes"
- Enter a natural language description:
  - _"upbeat songs about summer"_
  - _"melancholic indie tracks"_
  - _"energetic workout music"_
- Adjust the number of results
- View matches with similarity scores

## 🏗️ Architecture

```
vibra/
├── domain/           # Domain models (Track, SearchResult, etc.)
├── infrastructure/   # External integrations
│   ├── spotify/     # Spotify API client
│   ├── genius/      # Genius API client
│   ├── llm/         # Ollama LLM client
│   └── vectordb/    # ChromaDB repository
├── services/        # Business logic
│   ├── library_sync.py      # Sync and enrich tracks
│   ├── track_analysis.py    # AI vibe analysis
│   └── search.py            # Semantic search
├── ui/              # Streamlit interface
│   └── components/  # Reusable UI components
└── utils/           # Utilities (logging, settings)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
