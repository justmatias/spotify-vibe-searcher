"""Spotify API client wrapper using spotipy."""

from typing import Any

from pydantic import BaseModel
from spotipy import Spotify

from spotify_rag.domain import SavedTrack, SpotifyUser
from spotify_rag.domain.track import SpotifyArtist
from spotify_rag.utils.logger import LogLevel, log


class SpotifyClient(BaseModel):
    access_token: str

    @property
    def client(self) -> Spotify:
        return Spotify(auth=self.access_token)

    @property
    def current_user(self) -> SpotifyUser:
        user_data = self.client.current_user()
        return SpotifyUser.from_api_response(user_data)

    def get_liked_songs(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        return self.client.current_user_saved_tracks(  # type: ignore[no-any-return]
            limit=limit,
            offset=offset,
        )

    def get_all_liked_songs(self, max_tracks: int = 500) -> list[SavedTrack]:
        """Fetch all liked songs with pagination.

        Args:
            max_tracks: Maximum number of tracks to fetch.

        Returns:
            List of all saved track items.
        """
        log(f"Fetching up to {max_tracks} liked songs from Spotify...", LogLevel.INFO)

        all_tracks: list[SavedTrack] = []
        offset = 0
        limit = 50

        while offset < max_tracks:
            response = self.get_liked_songs(limit=limit, offset=offset)
            items = response.get("items", [])

            if items:
                all_tracks.extend(SavedTrack.from_api_response(item) for item in items)

            offset += limit

        total_fetched = len(all_tracks[:max_tracks])
        log(f"Successfully fetched {total_fetched} liked songs.", LogLevel.INFO)
        return all_tracks[:max_tracks]

    def get_artists(self, artist_ids: list[str]) -> list[SpotifyArtist]:
        """Fetch full artist details (including genres) in batches.

        Args:
            artist_ids: List of Spotify artist IDs.

        Returns:
            List of artist objects containing full metadata like genres.
        """
        batch_size = 50
        all_artists: list[SpotifyArtist] = []

        # Deduplicate IDs to save calls
        unique_ids = sorted(set(artist_ids))
        log(f"Fetching details for {len(unique_ids)} unique artists...", LogLevel.INFO)

        for i in range(0, len(unique_ids), batch_size):
            batch = unique_ids[i : i + batch_size]
            response = self.client.artists(batch)
            if response and "artists" in response:
                for artist in response["artists"]:
                    if artist:
                        all_artists.append(SpotifyArtist.from_api_response(artist))

        log(f"Retrieved details for {len(all_artists)} artists.", LogLevel.INFO)
        return all_artists
