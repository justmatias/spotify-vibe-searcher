from unittest.mock import MagicMock

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from spotify_rag.domain import (
    EnrichedTrack,
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
    SyncProgress,
)
from spotify_rag.infrastructure import GeniusClient, SpotifyClient, VectorDBRepository
from spotify_rag.injections import container
from spotify_rag.services import LibrarySyncService, TrackAnalysisService


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
def realistic_liked_songs(
    saved_track_factory: ModelFactory[SavedTrack],
    spotify_track_factory: ModelFactory[SpotifyTrack],
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
) -> list[SavedTrack]:
    return [
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Bohemian Rhapsody",
                artists=[
                    spotify_artist_factory.build(
                        name="Queen", genres=["rock", "classic rock"]
                    )
                ],
                album=spotify_album_factory.build(name="A Night at the Opera"),
                popularity=95,
            )
        ),
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Stairway to Heaven",
                artists=[
                    spotify_artist_factory.build(
                        name="Led Zeppelin", genres=["rock", "hard rock"]
                    )
                ],
                album=spotify_album_factory.build(name="Led Zeppelin IV"),
                popularity=92,
            )
        ),
        saved_track_factory.build(
            track=spotify_track_factory.build(
                name="Hotel California",
                artists=[
                    spotify_artist_factory.build(
                        name="Eagles", genres=["rock", "country rock"]
                    )
                ],
                album=spotify_album_factory.build(name="Hotel California"),
                popularity=90,
            )
        ),
    ]


@pytest.fixture
def mock_spotify_client(
    realistic_liked_songs: list[SavedTrack],
) -> MagicMock:
    client = MagicMock(spec=SpotifyClient)
    client.get_all_liked_songs.return_value = realistic_liked_songs
    return client


@pytest.fixture
def mock_genius_client() -> MagicMock:
    client = MagicMock(spec=GeniusClient)
    client.search_song.side_effect = [
        "First song lyrics",
        "Second song lyrics",
        "",
    ]
    return client


@pytest.fixture
def track_analysis_service() -> TrackAnalysisService:
    return container.services.track_analysis_service()  # type: ignore[no-any-return]


@pytest.fixture
def vectordb_repository() -> VectorDBRepository:
    return container.infrastructure.vectordb_repository()  # type: ignore[no-any-return]


@pytest.fixture
def library_sync_service(
    mock_spotify_client: MagicMock,
    mock_genius_client: MagicMock,
    track_analysis_service: TrackAnalysisService,
    vectordb_repository: VectorDBRepository,
) -> LibrarySyncService:
    return LibrarySyncService(
        spotify_client=mock_spotify_client,
        genius_client=mock_genius_client,
        track_analysis_service=track_analysis_service,
        vectordb_repository=vectordb_repository,
    )
