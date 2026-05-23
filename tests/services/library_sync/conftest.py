import uuid

import chromadb
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import (
    EnrichedTrack,
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
)
from vibra.infrastructure import (
    FakeGeniusClient,
    FakeLLMClient,
    FakeSpotifyClient,
    StubEmbeddingFunction,
    VectorDBRepository,
)
from vibra.services import (
    EnrichmentService,
    IndexingService,
    LibrarySyncService,
    TrackAnalysisService,
    TrackFetchService,
)


def make_library_sync_service(
    tracks: list[SavedTrack],
    lyrics_value: str = "Some lyrics content",
    vibe_value: str = "A vibe description.",
) -> LibrarySyncService:
    return LibrarySyncService(
        track_fetch=TrackFetchService(music_library=FakeSpotifyClient(tracks=tracks)),
        enrichment=EnrichmentService(
            lyrics=FakeGeniusClient(lyrics=lyrics_value),
            analyzer=TrackAnalysisService(
                llm_client=FakeLLMClient(response=vibe_value)
            ),
        ),
        indexing=IndexingService(
            store=VectorDBRepository(
                client=chromadb.EphemeralClient(),
                embedding_fn=StubEmbeddingFunction(),
                collection_name=str(uuid.uuid4()),
            )
        ),
    )


@pytest.fixture
def enriched_track_with_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        track=saved_track_factory.build(),
        lyrics="Test lyrics content",
    )


@pytest.fixture
def enriched_track_without_lyrics(
    enriched_track_factory: ModelFactory[EnrichedTrack],
    saved_track_factory: ModelFactory[SavedTrack],
) -> EnrichedTrack:
    return enriched_track_factory.build(
        track=saved_track_factory.build(),
        lyrics="",
    )


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
def library_sync_service(
    realistic_liked_songs: list[SavedTrack],
) -> LibrarySyncService:
    return make_library_sync_service(realistic_liked_songs)
