# pylint: disable=line-too-long
import asyncio
import uuid

import chromadb
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure import StubEmbeddingFunction, VectorDBRepository


@pytest.fixture
def vectordb_repository() -> VectorDBRepository:
    return VectorDBRepository(
        client=chromadb.EphemeralClient(),
        embedding_fn=StubEmbeddingFunction(),
        collection_name=str(uuid.uuid4()),
    )


@pytest.fixture
def enriched_track_with_vibe(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        track=saved_track_factory.build(),
        vibe_description="Generic vibe description for testing embeddings",
        has_lyrics=True,
    )


@pytest.fixture
def enriched_track_without_vibe(
    enriched_track_factory: ModelFactory[EnrichedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        vibe_description="",
        has_lyrics=False,
    )


@pytest.fixture
def enriched_tracks_batch(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[EnrichedTrack]:
    return [
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="Generic vibe 1",
            has_lyrics=True,
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="Generic vibe 2",
            has_lyrics=True,
        ),
        enriched_track_factory.build(
            vibe_description="",
            has_lyrics=False,
        ),
    ]


@pytest.fixture
def enriched_tracks_for_search(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[EnrichedTrack]:
    """Fixture with diverse vibe descriptions for search testing."""
    return [
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A melancholic indie track with introspective lyrics about lost love and regret",
            lyrics="Sample lyrics about heartbreak",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="An upbeat pop song with catchy hooks and positive energy perfect for dancing",
            lyrics="Sample lyrics about happiness",
        ),
        enriched_track_factory.build(
            track=saved_track_factory.build(),
            vibe_description="A dark and heavy metal track with aggressive guitar riffs and intense vocals",
            lyrics="Sample lyrics about anger",
        ),
    ]


@pytest.fixture
def _populate_with_single_track(
    vectordb_repository: VectorDBRepository,
    enriched_track_with_vibe: EnrichedTrack,
) -> None:
    asyncio.run(vectordb_repository.add(enriched_track_with_vibe))


@pytest.fixture
def _populate_with_batch(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_batch: list[EnrichedTrack],
) -> None:
    asyncio.run(vectordb_repository.add_many(enriched_tracks_batch))


@pytest.fixture
def _populate_with_search_tracks(
    vectordb_repository: VectorDBRepository,
    enriched_tracks_for_search: list[EnrichedTrack],
) -> None:
    asyncio.run(vectordb_repository.add_many(enriched_tracks_for_search))
