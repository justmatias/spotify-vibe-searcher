"""Library sync service for fetching and enriching Spotify tracks."""

import asyncio
from collections.abc import Generator
from itertools import batched

from pydantic import BaseModel

from spotify_vibe_searcher.domain import EnrichedTrack, SavedTrack, SyncProgress
from spotify_vibe_searcher.infrastructure import (
    GeniusClient,
    SpotifyClient,
    VectorDBRepository,
)
from spotify_vibe_searcher.utils import Settings
from spotify_vibe_searcher.utils.logger import LogLevel, log

from .track_analysis import TrackAnalysisService


class LibrarySyncService(BaseModel):
    spotify_client: SpotifyClient
    genius_client: GeniusClient
    track_analysis_service: TrackAnalysisService
    vectordb_repository: VectorDBRepository

    def sync_library(
        self, limit: int = 20
    ) -> Generator[SyncProgress | EnrichedTrack, None, None]:
        log(f"Starting library sync (limit={limit})...", LogLevel.INFO)

        saved_tracks = self.spotify_client.get_all_liked_songs(max_tracks=limit)
        self._enrich_artist_genres(saved_tracks)
        total = len(saved_tracks)
        log(f"Found {total} tracks to process.", LogLevel.INFO)

        current_index = 1
        for batch in batched(saved_tracks, Settings.LLM_CONCURRENCY_LIMIT):
            batch_tracks_for_processing = []

            for track in batch:
                yield SyncProgress(
                    current=current_index,
                    total=total,
                    song_title=track.track.name,
                    artist_name=track.track.artist_names,
                )
                current_index += 1
                batch_tracks_for_processing.append(track)

            enriched_tracks = asyncio.run(
                self._process_track_batch(batch_tracks_for_processing)
            )
            yield from enriched_tracks

        log("Library sync completed.", LogLevel.INFO)

    async def _process_track_batch(
        self, tracks: list[SavedTrack]
    ) -> list[EnrichedTrack]:
        tasks = [self._process_single_track(track) for track in tracks]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        # Filter out Nones
        return [result for result in results if result is not None]

    async def _process_single_track(
        self, saved_track: SavedTrack
    ) -> EnrichedTrack | None:
        track = saved_track.track
        exists = await asyncio.to_thread(
            self.vectordb_repository.track_exists, track.id_
        )
        if exists:
            log(f"Skipping '{track.name}' - already indexed.", LogLevel.DEBUG)
            return None

        try:
            enriched = await self._enrich_track(saved_track)
            if enriched.vibe_description:
                await asyncio.to_thread(self.vectordb_repository.add_track, enriched)
            return enriched
        except Exception as e:  # pragma: no cover
            log(f"Failed to enrich '{track.name}': {e}", LogLevel.WARNING)
            return None

    async def _enrich_track(self, saved_track: SavedTrack) -> EnrichedTrack:
        """Enrich a track with lyrics and vibe description asynchronously."""
        lyrics = await asyncio.to_thread(
            self.genius_client.search_song,
            title=saved_track.track.name,
            artist=saved_track.track.artist_names,
        )
        vibe_description = None

        if lyrics:
            vibe_description = await self.track_analysis_service.analyze_track(
                saved_track=saved_track,
                lyrics=lyrics,
            )

        return EnrichedTrack(
            track=saved_track,
            lyrics=lyrics,
            vibe_description=vibe_description,
        )

    def _enrich_artist_genres(self, saved_tracks: list[SavedTrack]) -> None:
        """Enrich artist data with genres by fetching full artist details"""
        artist_ids = [
            artist.id_
            for saved_track in saved_tracks
            for artist in saved_track.track.artists
        ]
        artists_with_genres = self.spotify_client.get_artists(artist_ids)
        artist_map = {artist.id_: artist for artist in artists_with_genres}

        for saved_track in saved_tracks:
            saved_track.track.artists = [
                artist_map.get(artist.id_, artist)
                for artist in saved_track.track.artists
            ]

        log(
            f"Enriched {len(artists_with_genres)} artists with genre data.",
            LogLevel.INFO,
        )
