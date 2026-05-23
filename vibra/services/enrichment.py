"""Service for enriching a track with lyrics and a vibe description."""

from pydantic import BaseModel, ConfigDict

from vibra.domain import EnrichedTrack, SavedTrack
from vibra.infrastructure.protocols import LyricsProvider
from vibra.utils import LogLevel, log

from .track_analysis import TrackAnalysisService


class EnrichmentService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    lyrics: LyricsProvider
    analyzer: TrackAnalysisService

    async def enrich(self, saved_track: SavedTrack) -> EnrichedTrack:
        track_lyrics = await self.lyrics.fetch(
            title=saved_track.track.name,
            artist=saved_track.track.artist_names,
        )
        vibe_description: str | None = None
        if track_lyrics:
            vibe_description = await self.analyzer.analyze_track(
                saved_track=saved_track,
                lyrics=track_lyrics,
            )
        else:
            log(
                f"No lyrics found for '{saved_track.track.name}' — skipping vibe analysis.",
                LogLevel.DEBUG,
            )

        return EnrichedTrack(
            track=saved_track,
            lyrics=track_lyrics,
            vibe_description=vibe_description,
        )
