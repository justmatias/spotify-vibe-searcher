"""ChromaDB vector database repository."""

from typing import Optional

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pydantic import BaseModel

from spotify_rag.domain import EnrichedTrack
from spotify_rag.utils import Settings


class VectorDBRepository(BaseModel):
    """Repository for ChromaDB vector database operations."""

    _client: Optional[PersistentClient] = None

    @property
    def client(self) -> PersistentClient:
        """Lazy-load persistent ChromaDB client."""
        if self._client is None:
            Settings.CHROMADB_PATH.mkdir(parents=True, exist_ok=True)
            self._client = PersistentClient(path=str(Settings.CHROMADB_PATH))
        return self._client

    @property
    def collection(self):
        return self.get_or_create_collection()

    def get_or_create_collection(self):
        """Get or create a collection by name with cosine similarity."""
        return self.client.get_or_create_collection(
            name=Settings.CHROMADB_COLLECTION,
            embedding_function=OllamaEmbeddingFunction(model=Settings.EMBEDDING_MODEL),
            metadata={"hnsw:space": "cosine"},  # Use cosine similarity
        )

    def add_track(self, enriched_track: EnrichedTrack) -> None:
        """Add a single enriched track to the collection."""
        if not enriched_track.vibe_description:
            return

        metadata = {
            "track_id": enriched_track.track_id,
            "track_name": enriched_track.track.name,
            "artist_names": enriched_track.track.artist_names,
            "album_name": enriched_track.track.album.name,
            "has_lyrics": enriched_track.has_lyrics,
            "genres": [
                genre
                for artist in enriched_track.track.artists
                for genre in artist.genres
            ],
            "popularity": enriched_track.track.popularity,
            "spotify_url": enriched_track.track.spotify_url or "",
        }

        self.collection.add(
            ids=[enriched_track.track_id],
            documents=[enriched_track.vibe_description],
            metadatas=[metadata],
        )

    def add_tracks(self, enriched_tracks: list[EnrichedTrack]) -> None:
        """Add multiple enriched tracks to the collection."""
        for enriched_track in enriched_tracks:
            self.add_track(enriched_track)

    def delete_tracks(self, track_ids: list[str]):
        self.collection.delete(ids=track_ids)
