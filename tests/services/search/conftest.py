import asyncio
import uuid

import chromadb
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure import (
    FakeLLMClient,
    StubEmbeddingFunction,
    VectorDBRepository,
)
from vibra.services import SearchService


@pytest.fixture
def vector_store() -> VectorDBRepository:
    return VectorDBRepository(
        client=chromadb.EphemeralClient(),
        embedding_fn=StubEmbeddingFunction(),
        collection_name=str(uuid.uuid4()),
    )


@pytest.fixture
def search_service(vector_store: VectorDBRepository) -> SearchService:
    return SearchService(
        vectordb_repository=vector_store,
        llm_client=FakeLLMClient(response="refined vibe query"),
    )


@pytest.fixture
def sample_query() -> str:
    return "sad melancholic songs about heartbreak"


@pytest.fixture
def _populate_search_tracks(
    vector_store: VectorDBRepository,
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> None:
    tracks = [
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="An upbeat pop song with catchy hooks and positive energy",
            lyrics="Sample lyrics about happiness",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A melancholic indie track with introspective lyrics about lost love",
            lyrics="Sample lyrics about heartbreak",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A dark heavy metal track with aggressive guitar riffs",
            lyrics="Sample lyrics about anger",
        ),
    ]
    asyncio.run(vector_store.add_many(tracks))
