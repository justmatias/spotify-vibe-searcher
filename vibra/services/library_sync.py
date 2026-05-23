"""Thin async-generator orchestrator for library sync."""

from collections.abc import AsyncGenerator

from pydantic import BaseModel

from vibra.domain import EnrichedTrack, SyncProgress
from vibra.utils import LogLevel, log

from .enrichment import EnrichmentService
from .indexing import IndexingService
from .track_fetch import TrackFetchService


class LibrarySyncService(BaseModel):
    track_fetch: TrackFetchService
    enrichment: EnrichmentService
    indexing: IndexingService

    async def sync_library(
        self, limit: int = 20
    ) -> AsyncGenerator[SyncProgress | EnrichedTrack, None]:
        log(f"Starting library sync (limit={limit})...", LogLevel.INFO)

        tracks = await self.track_fetch.fetch(limit)
        total = len(tracks)
        log(f"Found {total} tracks to process.", LogLevel.INFO)

        for i, saved_track in enumerate(tracks, start=1):
            yield SyncProgress(
                current=i,
                total=total,
                song_title=saved_track.track.name,
                artist_name=saved_track.track.artist_names,
            )

            if await self.indexing.is_indexed(saved_track.track.id_):
                log(
                    f"Skipping '{saved_track.track.name}' — already indexed.",
                    LogLevel.DEBUG,
                )
                continue

            enriched = await self.enrichment.enrich(saved_track)
            await self.indexing.index(enriched)
            yield enriched

        log("Library sync completed.", LogLevel.INFO)
