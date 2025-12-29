"""Library sync service for fetching and enriching Spotify tracks."""

from collections.abc import Generator

from pydantic import BaseModel

from spotify_rag.domain import EnrichedTrack, SyncProgress
from spotify_rag.infrastructure import GeniusClient, SpotifyClient


class LibrarySyncService(BaseModel):
    """Service to orchestrate fetching tracks and enriching with lyrics."""

    spotify_client: SpotifyClient
    genius_client: GeniusClient

    def sync_library(
        self, limit: int = 20
    ) -> Generator[SyncProgress | EnrichedTrack, None, None]:
        """Sync library by fetching tracks and lyrics.

        Args:
            limit: Maximum number of tracks to process.

        Yields:
            SyncProgress: Progress updates during processing.
            EnrichedTrack: Enriched track with lyrics.
        """
        saved_tracks = self.spotify_client.get_all_liked_songs(max_tracks=limit)

        total = len(saved_tracks)

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

            lyrics = self.genius_client.search_song(
                title=song_title,
                artist=artist_name,
            )

            has_lyrics = bool(lyrics)

            yield EnrichedTrack(
                track=saved_track,
                lyrics=lyrics,
                has_lyrics=has_lyrics,
            )
