"""Fixtures for track analysis service tests."""

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import SavedTrack
from vibra.infrastructure import FakeLLMClient
from vibra.injections import TestContainer
from vibra.services import TrackAnalysisService


@pytest.fixture
def llm_client(test_container: TestContainer) -> FakeLLMClient:
    return test_container.infrastructure.llm_client()  # type: ignore[no-any-return]


@pytest.fixture
def track_analysis_service(test_container: TestContainer) -> TrackAnalysisService:
    return test_container.services.track_analysis_service()  # type: ignore[no-any-return]


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
