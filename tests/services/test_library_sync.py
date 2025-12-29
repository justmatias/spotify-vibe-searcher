"""Tests for LibrarySyncService."""

from unittest.mock import MagicMock

from spotify_rag.domain import EnrichedTrack, SyncProgress
from spotify_rag.services import LibrarySyncService


def test_sync_library_yields_progress_and_tracks(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    assert isinstance(results[0], SyncProgress)
    assert isinstance(results[1], EnrichedTrack)


def test_sync_library_progress_increments(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    progress_updates = [r for r in results if isinstance(r, SyncProgress)]

    assert len(progress_updates) == 3
    assert progress_updates[0].current == 1
    assert progress_updates[1].current == 2
    assert progress_updates[2].current == 3
    assert all(p.total == 3 for p in progress_updates)


def test_sync_library_tracks_with_and_without_lyrics(
    library_sync_service: LibrarySyncService,
) -> None:
    results = list(library_sync_service.sync_library(limit=3))

    enriched_tracks = [
        result for result in results if isinstance(result, EnrichedTrack)
    ]

    assert len(enriched_tracks) == 3

    assert enriched_tracks[0].has_lyrics
    assert enriched_tracks[0].lyrics == "First song lyrics"

    assert enriched_tracks[1].has_lyrics
    assert enriched_tracks[1].lyrics == "Second song lyrics"

    assert not enriched_tracks[2].has_lyrics
    assert not enriched_tracks[2].lyrics


def test_sync_library_calls_spotify_client(
    library_sync_service: LibrarySyncService,
    mock_spotify_client: MagicMock,
) -> None:
    list(library_sync_service.sync_library(limit=5))

    mock_spotify_client.get_all_liked_songs.assert_called_once_with(max_tracks=5)


def test_sync_library_calls_genius_client_for_each_track(
    library_sync_service: LibrarySyncService,
    mock_genius_client: MagicMock,
) -> None:
    list(library_sync_service.sync_library(limit=3))

    assert mock_genius_client.search_song.call_count == 3


def test_enriched_track_properties(
    enriched_track_with_lyrics: EnrichedTrack,
    enriched_track_without_lyrics: EnrichedTrack,
) -> None:
    assert enriched_track_with_lyrics.has_lyrics
    assert len(enriched_track_with_lyrics.lyrics) > 0
    assert enriched_track_with_lyrics.track

    assert not enriched_track_without_lyrics.has_lyrics
    assert not enriched_track_without_lyrics.lyrics
