# 🎵 Project: Spotify Semantic Vibe Searcher (RAG)

## 📋 Overview

This project aims to build a semantic search engine for your "Liked Songs" on Spotify. Instead of searching by keywords (Artist/Title), users can search by **vibe, mood, or abstract scenarios** (e.g., _"music for coding late at night"_).

**Core Concept:** Convert numerical audio features (`valence`, `energy`, etc.) into natural language descriptions, embed them, and use RAG to retrieve and recommend songs.

---

## 🛠 Tech Stack

- **Language:** Python 3.12+
- **Orchestration:** `LangChain`
- **Vector Database:** `ChromaDB` (Local, persistent, lightweight)
- **Embeddings & LLM:** `OpenAI` (`text-embedding-3-small` / `gpt-4o-mini`) OR `Ollama` (local Llama 3)
- **Data Validation:** `Pydantic` (Great for structuring the Spotify data)

---

## 📅 Implementation Phases

### Phase 1: Environment & Authentication

Setup the foundational connection to Spotify.

1. **Spotify App Setup:**

- Go to [Spotify for Developers](https://developer.spotify.com/dashboard).
- Create an app to get `CLIENT_ID` and `CLIENT_SECRET`.
- Set Redirect URI (e.g., `http://localhost:8888/callback`).

2. **Project Setup:**

- Initialize git repo.
- Create `.env` file for API keys.
- Dependencies: `uv add spotipy chromadb langchain langchain-openai pydantic`

### Phase 2: Data Ingestion (ETL)

Extract raw data and enrich it with audio features.

1. **Fetch Liked Songs:**

- Use `sp.current_user_saved_tracks()`.
- _Note:_ Handle pagination to get your full library (or limit to the last 500 for testing).

2. **Fetch Audio Features:**

- Collect Track IDs from the previous step.
- Use `sp.audio_features(track_ids)` (Batch this! Spotify accepts up to 100 IDs per call).

3. **Data Merging:**

- Create a clean list of dictionaries merging metadata (Name, Artist) with features (Tempo, Energy, Valence).

### Phase 3: The "Semantic Bridge" (Critical Step)

This is where you solve the "translation" problem. You cannot embed raw numbers effectively; you need text.

1. **Feature-to-Text Logic:**

- Write a helper function `generate_track_description(track_data)`.
- **Logic Example:**
- If `valence < 0.3` → "Melancholic/Sad"
- If `energy > 0.8` → "High intensity, explosive"
- If `acousticness > 0.8` → "Raw, acoustic instrumentals"

2. **Synthetic Metadata Generation:**

- Construct a final string for each song.
- _Format:_ `"Song: {title} by {artist}. Genre: {genre}. A {mood} track with {intensity} energy. It feels {adjective}."`
- _Why?_ When the user asks for "sad music," the vector search matches the word "sad" or "melancholic" in this synthetic string.

### Phase 4: Vector Storage (RAG Backend)

Store the semantic representations.

1. **Initialize ChromaDB:**

- Create a persistent client: `chromadb.PersistentClient(path="./db")`.

2. **Embedding:**

- Use an embedding model (e.g., OpenAI `text-embedding-3-small`).
- **Document:** The synthetic text string from Phase 3.
- **Metadata:** Store the JSON payload (`track_id`, `uri`, `artist_name`) here so you can retrieve the link later.

3. **Upsert:**

- Add the documents to the collection.

### Phase 5: The Retrieval Pipeline

Build the interaction loop.

1. **User Input:** Accept a query (e.g., _"I need focus music for coding"_).
2. **Semantic Search:**

- Embed the query.
- Query ChromaDB for the `top_k=5` closest matches.

3. **LLM Generation (The "DJ"):**

- Construct a prompt context with the retrieved songs.
- **Prompt Template:**
  > "You are a personalized DJ. The user asked for: '{user_query}'.
  > Based on their library, here are the best matches:
  > {retrieved_songs_list}
  > Create a short playlist recommendation explaining why these specific songs fit the requested vibe."

### Phase 6: Streamlit UI & OAuth (The Frontend)

Integrate the UI and handle the login flow.

1. **Authentication (The trickiest part):**

- Use `spotipy.oauth2.SpotifyOAuth`.
- Check `st.session_state` for a token. If not present, show a "Login with Spotify" button that redirects to the auth URL.
- Once redirected back, parse the code from the URL parameters to get the token.

2. **The "Ingest" Button:**

- Show a button: "Analyze my Library".
- On click: Run Phase 2 & 3 scripts. Show a progress bar (`st.progress`).
- _Tip:_ Cache this data or check if it already exists in ChromaDB to avoid re-running it every time.

3. **Chat Interface:**

- Use `st.chat_input` for the user query (e.g., "Music for a rainy day").
- Display the LLM response using `st.write`.
- **Visuals:** Use `st.image` to show the album art of the recommended songs next to the text.

---

## 📂 Recommended Directory Structure

```text
spotify-rag/
├── data/                  # ChromaDB storage
├── src/
│   ├── auth/
│   │   └── oauth.py       # Streamlit-specific Auth logic
│   ├── etl/
│   │   ├── extract.py     # Spotify API calls
│   │   └── transform.py   # Semantic description logic
│   ├── rag/
│   │   ├── vector_store.py
│   │   └── chain.py       # LangChain setup
│   └── ui/
│       └── components.py  # Reusable UI widgets (e.g., song cards)
├── app.py                 # Main Streamlit Entry point
├── .env
├── requirements.txt
└── README.md

```

## 🚀 Definition of Done (MVP)

1. Open `localhost:8501`.
2. Click "Login with Spotify" (Redirects and returns).
3. Click "Analyze Library" (Progress bar fills up).
4. Type "I need high energy music for the gym" in the chat box.
5. Receive a text response + 5 Album covers of songs _actually_ in your library.

```

```
