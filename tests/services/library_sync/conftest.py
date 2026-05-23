"""Fixtures for library sync service tests."""

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain import (
    EnrichedTrack,
    IndexedTrack,
    SavedTrack,
    SearchResults,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
)
from vibra.services import (
    EnrichmentService,
    IndexingService,
    LibrarySyncService,
    TrackAnalysisService,
    TrackFetchService,
)


@dataclass
class InMemoryVectorStore:
    """In-process fake implementing the VectorStore protocol."""

    _store: dict[str, EnrichedTrack] = field(default_factory=dict)

    async def track_exists(self, track_id: str) -> bool:
        return track_id in self._store

    async def add(self, track: EnrichedTrack) -> None:
        self._store[track.track_id] = track

    async def add_many(self, tracks: list[EnrichedTrack]) -> None:
        for track in tracks:
            self._store[track.track_id] = track

    async def search(self, query: str, n_results: int) -> SearchResults:  # pylint: disable=unused-argument
        raise NotImplementedError  # pragma: no cover

    async def count(self) -> int:
        return len(self._store)

    async def delete(self, ids: list[str]) -> None:
        for id_ in ids:
            self._store.pop(id_, None)

    async def list_all(self) -> list[IndexedTrack]:
        raise NotImplementedError  # pragma: no cover


@dataclass
class FakeMusicLibrary:
    """In-process fake implementing the MusicLibrary protocol."""

    tracks: list[SavedTrack] = field(default_factory=list)

    async def read_liked_songs(self, max_tracks: int) -> AsyncIterator[SavedTrack]:
        async def _gen() -> AsyncIterator[SavedTrack]:
            for t in self.tracks[:max_tracks]:
                yield t

        return _gen()

    async def get_artists(self, ids: list[str]) -> list[SpotifyArtist]:
        artist_map = {a.id_: a for t in self.tracks for a in t.track.artists}
        return [artist_map[id_] for id_ in ids if id_ in artist_map]

    async def current_user(self) -> Any:  # pragma: no cover
        raise NotImplementedError


@dataclass
class FakeLyricsProvider:
    """In-process fake implementing the LyricsProvider protocol."""

    return_value: str = "Some lyrics content"

    async def fetch(self, *, title: str, artist: str) -> str:  # pylint: disable=unused-argument
        return self.return_value


@dataclass
class FakeLLMProvider:
    """In-process fake implementing the LLMProvider protocol."""

    return_value: str = "A vibe description."

    async def generate(self, prompt: str) -> str:  # pylint: disable=unused-argument
        return self.return_value


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


def make_library_sync_service(
    tracks: list[SavedTrack],
    lyrics_value: str = "Some lyrics content",
    vibe_value: str = "A vibe description.",
) -> LibrarySyncService:
    return LibrarySyncService(
        track_fetch=TrackFetchService(music_library=FakeMusicLibrary(tracks=tracks)),
        enrichment=EnrichmentService(
            lyrics=FakeLyricsProvider(return_value=lyrics_value),
            analyzer=TrackAnalysisService(llm_client=FakeLLMProvider(return_value=vibe_value)),
        ),
        indexing=IndexingService(store=InMemoryVectorStore()),
    )


@pytest.fixture
def library_sync_service(
    realistic_liked_songs: list[SavedTrack],
) -> LibrarySyncService:
    return make_library_sync_service(realistic_liked_songs)
