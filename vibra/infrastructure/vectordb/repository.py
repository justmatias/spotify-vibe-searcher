"""ChromaDB vector database repository."""

import asyncio
from functools import cached_property

import stamina
from chromadb import Collection, PersistentClient
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from pydantic import BaseModel

from vibra.domain import EnrichedTrack, IndexedTrack, SearchResults
from vibra.utils import LogLevel, Settings, log

from .config import RETRY_ON
from .mappers import (
    chroma_get_to_indexed_tracks,
    chroma_query_to_results,
    enriched_to_payload,
)


class VectorDBRepository(BaseModel):
    """Repository for ChromaDB vector database operations."""

    @cached_property
    def collection(self) -> Collection:
        Settings.CHROMADB_PATH.mkdir(parents=True, exist_ok=True)
        log(
            f"Initializing ChromaDB client at {Settings.CHROMADB_PATH}",
            LogLevel.INFO,
        )
        client = PersistentClient(path=str(Settings.CHROMADB_PATH))
        return client.get_or_create_collection(
            name=Settings.CHROMADB_COLLECTION,
            embedding_function=OllamaEmbeddingFunction(
                model_name=Settings.EMBEDDING_MODEL
            ),
            metadata={"hnsw:space": "cosine"},
        )

    async def track_exists(self, track_id: str) -> bool:
        result = await asyncio.to_thread(self._get_ids, track_id)
        return len(result) > 0

    async def add(self, track: EnrichedTrack) -> None:
        if not track.vibe_description:
            return
        payload = enriched_to_payload(track)
        log(
            f"Storing track '{track.track.track.name}'",
            LogLevel.DEBUG,
        )
        await asyncio.to_thread(
            self._add_to_collection,
            payload["ids"],
            payload["documents"],
            payload["metadatas"],
        )

    async def add_many(self, tracks: list[EnrichedTrack]) -> None:
        valid = [t for t in tracks if t.vibe_description]
        if not valid:
            return
        log(f"Adding {len(valid)} tracks to VectorDB...", LogLevel.INFO)
        ids, documents, metadatas = [], [], []
        for track in valid:
            payload = enriched_to_payload(track)
            ids.extend(payload["ids"])
            documents.extend(payload["documents"])
            metadatas.extend(payload["metadatas"])
        await asyncio.to_thread(self._add_to_collection, ids, documents, metadatas)
        log("Successfully added tracks to VectorDB.", LogLevel.INFO)

    async def search(self, query: str, n_results: int = 10) -> SearchResults:
        log(f"Searching for vibe: '{query}'", LogLevel.INFO)
        raw = await asyncio.to_thread(self._query_collection, query, n_results)
        results = chroma_query_to_results(query, raw)
        log(f"Found {results.total_results} matching tracks", LogLevel.INFO)
        return results

    async def count(self) -> int:
        return await asyncio.to_thread(self.collection.count)

    async def delete(self, ids: list[str]) -> None:
        log(f"Deleting {len(ids)} tracks from VectorDB...", LogLevel.INFO)
        await asyncio.to_thread(self.collection.delete, ids)

    async def list_all(self) -> list[IndexedTrack]:
        log("Retrieving all indexed tracks from VectorDB...", LogLevel.INFO)
        raw = await asyncio.to_thread(self.collection.get)
        return chroma_get_to_indexed_tracks(raw)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _get_ids(self, track_id: str) -> list[str]:
        result: dict[str, list] = self.collection.get(ids=[track_id])
        return result["ids"]

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _add_to_collection(
        self,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _query_collection(self, query: str, n_results: int) -> dict[str, list]:
        return self.collection.query(query_texts=[query], n_results=n_results)  # type: ignore[no-any-return]
