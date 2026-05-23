import pytest

from vibra.domain import EnrichedTrack, SavedTrack, SyncProgress
from vibra.services import LibrarySyncService

from .conftest import make_library_sync_service


@pytest.mark.asyncio
async def test_sync_library_yields_progress_and_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = [item async for item in library_sync_service.sync_library(limit=3)]

    assert any(isinstance(r, SyncProgress) for r in results)
    assert any(isinstance(r, EnrichedTrack) for r in results)


@pytest.mark.asyncio
async def test_sync_library_progress_increments(
    library_sync_service: LibrarySyncService,
) -> None:
    results = [item async for item in library_sync_service.sync_library(limit=3)]

    progress_updates = [r for r in results if isinstance(r, SyncProgress)]

    assert len(progress_updates) == 3
    assert progress_updates[0].current == 1
    assert progress_updates[1].current == 2
    assert progress_updates[2].current == 3
    assert all(p.total == 3 for p in progress_updates)


@pytest.mark.asyncio
async def test_sync_library_enriches_all_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = [item async for item in library_sync_service.sync_library(limit=3)]

    enriched_tracks = [r for r in results if isinstance(r, EnrichedTrack)]

    assert len(enriched_tracks) == 3
    assert all(t.has_lyrics for t in enriched_tracks)
    assert all(t.vibe_description for t in enriched_tracks)


@pytest.mark.asyncio
async def test_sync_library_skips_already_indexed_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    # First sync indexes everything.
    await _collect(library_sync_service, limit=3)

    # Second sync — all tracks already indexed, none yielded as EnrichedTrack.
    results = [item async for item in library_sync_service.sync_library(limit=3)]

    assert len([r for r in results if isinstance(r, SyncProgress)]) == 3
    assert len([r for r in results if isinstance(r, EnrichedTrack)]) == 0


@pytest.mark.asyncio
async def test_sync_library_without_lyrics_skips_vibe_analysis(
    realistic_liked_songs: list[SavedTrack],
) -> None:
    service = make_library_sync_service(realistic_liked_songs, lyrics_value="")

    results = [item async for item in service.sync_library(limit=1)]

    enriched_tracks = [r for r in results if isinstance(r, EnrichedTrack)]

    assert len(enriched_tracks) == 1
    assert not enriched_tracks[0].has_lyrics
    assert enriched_tracks[0].vibe_description is None


def test_enriched_track_properties(
    enriched_track_with_lyrics: EnrichedTrack,
    enriched_track_without_lyrics: EnrichedTrack,
) -> None:
    assert enriched_track_with_lyrics.has_lyrics
    assert len(enriched_track_with_lyrics.lyrics) > 0

    assert not enriched_track_without_lyrics.has_lyrics
    assert not enriched_track_without_lyrics.lyrics


async def _collect(
    service: LibrarySyncService, *, limit: int
) -> list[SyncProgress | EnrichedTrack]:
    return [item async for item in service.sync_library(limit=limit)]
