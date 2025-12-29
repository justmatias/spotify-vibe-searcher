from unittest.mock import MagicMock

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from spotify_rag.domain import EnrichedTrack, SavedTrack, SyncProgress
from spotify_rag.infrastructure import GeniusClient, SpotifyClient
from spotify_rag.services import LibrarySyncService


@register_fixture(name="saved_track_factory")
class SavedTrackFactory(ModelFactory[SavedTrack]): ...


@register_fixture(name="sync_progress_factory")
class SyncProgressFactory(ModelFactory[SyncProgress]): ...


@register_fixture(name="enriched_track_factory")
class EnrichedTrackFactory(ModelFactory[EnrichedTrack]): ...


@pytest.fixture
def sync_progress_sample(
    sync_progress_factory: ModelFactory[SyncProgress],
) -> SyncProgress:
    return sync_progress_factory.build(
        current=1,
        total=10,
        song_title="Test Song",
        artist_name="Test Artist",
    )


@pytest.fixture
def enriched_track_with_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    track = saved_track_factory.build()
    return enriched_track_factory.build(
        track=track,
        lyrics="Test lyrics content",
        has_lyrics=True,
    )


@pytest.fixture
def enriched_track_without_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    track = saved_track_factory.build()
    return enriched_track_factory.build(
        track=track,
        lyrics="",
        has_lyrics=False,
    )


@pytest.fixture
def liked_songs(
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[SavedTrack]:
    return [saved_track_factory.build() for _ in range(3)]


@pytest.fixture
def liked_songs_lyrics(
    saved_track_factory: ModelFactory[SavedTrack],
) -> list[SavedTrack]:
    return [saved_track_factory.build() for _ in range(3)]


@pytest.fixture
def mock_spotify_client(
    liked_songs: list[SavedTrack],
) -> MagicMock:
    client = MagicMock(spec=SpotifyClient)
    client.get_all_liked_songs.return_value = liked_songs
    return client


@pytest.fixture
def mock_genius_client() -> MagicMock:
    """Create a mock GeniusClient."""
    client = MagicMock(spec=GeniusClient)
    client.search_song.side_effect = [
        "First song lyrics",
        "Second song lyrics",
        "",
    ]
    return client


@pytest.fixture
def library_sync_service(
    mock_spotify_client: MagicMock,
    mock_genius_client: MagicMock,
) -> LibrarySyncService:
    """Create LibrarySyncService with mocked dependencies."""
    return LibrarySyncService(
        spotify_client=mock_spotify_client,
        genius_client=mock_genius_client,
    )
