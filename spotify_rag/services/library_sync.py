"""Library sync service for fetching and enriching Spotify tracks."""

from collections.abc import Generator

from pydantic import BaseModel

from spotify_rag.domain import EnrichedTrack, SavedTrack, SyncProgress
from spotify_rag.infrastructure import GeniusClient, SpotifyClient, VectorDBRepository
from spotify_rag.utils.logger import LogLevel, log

from .track_analysis import TrackAnalysisService


class LibrarySyncService(BaseModel):
    """Service to orchestrate fetching tracks and enriching with lyrics."""

    spotify_client: SpotifyClient
    genius_client: GeniusClient
    track_analysis_service: TrackAnalysisService
    vectordb_repository: VectorDBRepository

    def sync_library(
        self, limit: int = 20
    ) -> Generator[SyncProgress | EnrichedTrack, None, None]:
        """Sync library by fetching tracks, lyrics, and generating AI analysis.

        Args:
            limit: Maximum number of tracks to process.

        Yields:
            SyncProgress: Progress updates during processing.
            EnrichedTrack: Enriched track with lyrics and vibe description.
        """
        log(f"Starting library sync (limit={limit})...", LogLevel.INFO)

        saved_tracks = self.spotify_client.get_all_liked_songs(max_tracks=limit)
        total = len(saved_tracks)
        log(f"Found {total} tracks to process.", LogLevel.INFO)

        for idx, saved_track in enumerate(saved_tracks, start=1):
            track = saved_track.track
            song_title = track.name
            artist_name = track.artist_names

            yield SyncProgress(
                current=idx,
                total=total,
                song_title=song_title,
                artist_name=artist_name,
            )

            enriched_track = self.enrich_track(saved_track)
            if enriched_track.vibe_description:
                self.vectordb_repository.add_track(enriched_track)

            yield enriched_track

        log("Library sync completed.", LogLevel.INFO)

    def enrich_track(self, saved_track: SavedTrack) -> EnrichedTrack:
        """Enrich a track with lyrics and vibe description."""
        lyrics = self.genius_client.search_song(
            title=saved_track.track.name,
            artist=saved_track.track.artist_names,
        )

        vibe_description = None
        if lyrics:
            vibe_description = self.track_analysis_service.analyze_track(
                saved_track=saved_track,
                lyrics=lyrics,
            )

        return EnrichedTrack(
            track=saved_track,
            lyrics=lyrics,
            vibe_description=vibe_description,
        )
