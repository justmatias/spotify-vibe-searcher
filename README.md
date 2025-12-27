# 🎵 Spotify Semantic Vibe Searcher (RAG)

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![Spotify API](https://img.shields.io/badge/Spotify-API-1DB954)

> **Stop searching by Genre. Start searching by *Vibe*.**

This project is a **Retrieval-Augmented Generation (RAG)** application that allows you to search your personal Spotify "Liked Songs" library using natural language abstract descriptions (e.g., *"Songs for coding late at night while it's raining"*).

It bridges the gap between raw **Audio Features** (numbers) and **Human Language** (semantics) to provide personalized recommendations from your own library.

## 🧠 How it Works

Standard Spotify search relies on keywords (Artist, Track Name, Genre). This project uses a **RAG pipeline**:

1.  **Extraction (ETL):** Fetches your *Liked Songs* and their specific *Audio Features* (Valence, Energy, Danceability, etc.) via the Spotify API.
2.  **Semantic Translation:** Converts numerical features into a descriptive natural language paragraph (The "Semantic Bridge").
    * *Example:* `valence: 0.1, energy: 0.2` $\rightarrow$ *"A deeply melancholic and low-energy track, suitable for introspection."*
3.  **Embedding:** Vectorizes these descriptions using embeddings and stores them in **ChromaDB**.
4.  **Retrieval & Generation:**
    * The user queries: *"I need music to fight a final boss."*
    * The system performs a vector similarity search.
    * The **LLM (DJ)** receives the top matches and explains *why* they fit the requested mood.

## 🛠️ Tech Stack

* **Language:** Python 3.12+
* **Data Source:** [Spotify Web API](https://developer.spotify.com/documentation/web-api) (via `spotipy`)
* **Vector Database:** [ChromaDB](https://www.trychroma.com/) (Local persistence)
* **LLM & Embeddings:** OpenAI (GPT-4o / text-embedding-3) OR LangChain
* **Data Validation:** Pydantic