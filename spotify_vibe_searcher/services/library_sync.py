"""Library sync service for fetching and enriching Spotify tracks."""

from collections.abc import Generator

from pydantic import BaseModel

from spotify_vibe_searcher.domain import EnrichedTrack, SavedTrack, SyncProgress
from spotify_vibe_searcher.infrastructure import (
    GeniusClient,
    SpotifyClient,
    VectorDBRepository,
)
from spotify_vibe_searcher.utils.logger import LogLevel, log

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

        self._enrich_artist_genres(saved_tracks)

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

            if self.vectordb_repository.track_exists(track.id_):
                log(
                    f"Skipping '{song_title}' - already indexed.",
                    LogLevel.INFO,
                )
                continue

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

    def _enrich_artist_genres(self, saved_tracks: list[SavedTrack]) -> None:
        """Enrich artist data with genres by fetching full artist details"""
        artist_ids = []
        for saved_track in saved_tracks:
            for artist in saved_track.track.artists:
                artist_ids.append(artist.id_)

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
