"""Fixtures for VectorDB repository tests."""

import pathlib
from collections.abc import Generator

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from spotify_rag.domain import EnrichedTrack, SavedTrack
from spotify_rag.infrastructure import VectorDBRepository
from spotify_rag.utils import Settings


@pytest.fixture
def vectordb_repository(tmp_path: pathlib.Path) -> Generator[VectorDBRepository]:
    original_data_dir = Settings.DATA_DIR
    Settings.DATA_DIR = tmp_path
    yield VectorDBRepository()
    Settings.DATA_DIR = original_data_dir


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
