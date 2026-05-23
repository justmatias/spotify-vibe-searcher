"""Fixtures for track analysis service tests."""

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import SavedTrack
from vibra.infrastructure import FakeLLMClient
from vibra.services import TrackAnalysisService


@pytest.fixture
def llm_client() -> FakeLLMClient:
    return FakeLLMClient(response="An indie rock track with nostalgic themes and emotional depth.")


@pytest.fixture
def track_analysis_service(llm_client: FakeLLMClient) -> TrackAnalysisService:
    return TrackAnalysisService(llm_client=llm_client)


@pytest.fixture
def sample_saved_track(
    saved_track_factory: ModelFactory[SavedTrack],
) -> SavedTrack:
    return saved_track_factory.build()


@pytest.fixture
def sample_lyrics() -> str:
    return "Test lyrics about love and loss"


@pytest.fixture
def simple_lyrics() -> str:
    return "Test lyrics"
