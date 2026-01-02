# 🎵 Project: Spotify Semantic Search (Deep Lyrics Edition)

## 📋 Overview

This project builds a semantic search engine for your Spotify "Liked Songs" library. It overcomes the deprecation of Spotify's Audio Features API and the lack of emotional context by combining three data sources:

1. **Spotify:** Base metadata (Title, Artist, Album).
2. **Genius:** Full song lyrics.
3. **LLM (AI):** Analyzes the cognitive dissonance between the musical genre and the lyrical meaning (e.g., "Happy sounding music with sad lyrics").

---

## 🛠 Tech Stack

- **Language:** Python 3.12+
- **Package Manager:** `uv`
- **Orchestration:** `LangChain`
- **Vector Database:** `ChromaDB` (Local, persistent)
- **Data Sources:**
- `spotipy` (Spotify Web API)
- `lyricsgenius` (Genius API wrapper)

- **Frontend:** `Streamlit`

---

## 📅 Implementation Phases

### Phase 1: Environment & Credentials (x2)

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

### Phase 2: Data Ingestion (The Bottleneck)

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

### Phase 3: Deep Vibe Enrichment

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

### Phase 4: Vector Storage

Similar to the previous plan, but the embedding quality will be superior.

1. **Embed:** Use `text-embedding-3-small` on the generated description.
2. **Metadata:** Store `has_lyrics: bool` in ChromaDB so you can filter later if desired.

### Phase 5: Retrieval & Chat

The search flow remains, but the "DJ" response will be smarter.

1. **Query:** "I want songs that sound happy but are deep down sad."
2. **Match:** Thanks to the Phase 3 analysis, the system will find those songs with cognitive dissonance.
3. **Response:** The LLM can quote a line from the lyrics to justify its choice.

### Phase 6: UI with Progress Feedback

Since Genius is slow, the UI is critical.

1. **Real Progress Bar:**

- In Streamlit, use `my_bar = st.progress(0)`.
- Update the bar for each processed song (Spotify + Genius + OpenAI).

2. **Limit Control:**

- Add a `slider` in the UI: _"How many recent songs to analyze?"_ (Default: 20, Max: 100).
- _Warning:_ "Analyzing lyrics takes time (approx 2-3 seconds per song)."

3. **Display:**

- Show the song card, and if lyrics were found, add a small _expander_ labeled "See AI Analysis" to show the generated explanation.

```

## 🚀 Definition of Done (Pro Level)

1. **Login:** User logs in via Spotify.
2. **Config:** Select "Analyze last 10 songs".
3. **Wait:** User sees the progress bar advance while logs show _"Downloading lyrics for 'Bohemian Rhapsody'..."_.
4. **Chat:** User asks _"Which songs talk about making a mistake?"_.
5. **Result:** App returns specific songs based on lyrical content, not just the title.
```

## 🚀 Future Potential Features

### Short Term (Usability)

- [ ] **Playlist Creation**: One-click "Create Playlist" from search results directly to Spotify.
- [ ] **Filters**: Add explicit filters for Genre, Year, or BPM range to narrow down semantic search.
- [ ] **Audio Preview**: Embedded Spotify web player widget to preview tracks instantly.

### Medium Term (Performance & Scale)

- [ ] **Async Batching**: optimize LLM inference by batching requests or running parallel processing for larger libraries.
- [x] **Caching Strategy**: Implement a more aggressive caching layer for Genius lyrics to reduce API hits on re-syncs.
- [x] **Incremental Sync**: Only analyze _newly added_ tracks instead of re-scanning the last N tracks every time.

### Long Term (AI & Experience)

- [ ] **Personalized Vibe Models**: Fine-tune a small LoRA adapter on the user's specific taste descriptions.
- [ ] **Voice Search**: "Hey, play me something for a rainy Sunday."
- [ ] **Multi-Modal Input**: Upload a photo (e.g., a sunset) and get songs that match the visual vibe (using LLaVA or similar vision models).
