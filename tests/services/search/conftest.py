"""Fixtures for search service tests."""

import asyncio

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure import VectorDBRepository
from vibra.injections import TestContainer
from vibra.services import SearchService


@pytest.fixture
def vector_store(test_container: TestContainer) -> VectorDBRepository:
    return test_container.infrastructure.vectordb_repository()


@pytest.fixture
def search_service(test_container: TestContainer) -> SearchService:
    return test_container.services.search_service()


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
