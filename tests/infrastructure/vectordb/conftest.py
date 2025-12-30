"""Fixtures for VectorDB repository tests."""

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from spotify_rag.domain import EnrichedTrack, SavedTrack
from spotify_rag.infrastructure import VectorDBRepository


@pytest.fixture
def vectordb_repository() -> VectorDBRepository:
    return VectorDBRepository()


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
