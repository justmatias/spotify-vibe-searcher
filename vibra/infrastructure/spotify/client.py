import asyncio
from collections.abc import AsyncIterator
from functools import cached_property
from itertools import batched
from typing import Any

import stamina
from pydantic import BaseModel
from spotipy import Spotify

from vibra.domain import SavedTrack, SpotifyArtist, SpotifyUser
from vibra.utils import LogLevel, log

from .config import RETRY_ON
from .mappers import to_artist, to_saved_track, to_user


class SpotifyClient(BaseModel):
    access_token: str

    @cached_property
    def client(self) -> Spotify:
        return Spotify(auth=self.access_token)

    async def current_user(self) -> SpotifyUser:
        user_data = await asyncio.to_thread(self._fetch_current_user)
        return to_user(user_data)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _fetch_current_user(self) -> dict[str, Any]:
        return self.client.current_user()  # type: ignore[no-any-return]

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _fetch_page(self, limit: int = 50, offset: int = 0) -> dict[str, Any]:
        return self.client.current_user_saved_tracks(limit=limit, offset=offset)  # type: ignore[no-any-return]

    async def read_liked_songs(
        self, max_tracks: int = 500
    ) -> AsyncIterator[SavedTrack]:
        offset = 0
        yielded = 0
        while offset < max_tracks:
            page = await asyncio.to_thread(self._fetch_page, 50, offset)
            items = page.get("items", [])
            if not items:
                break
            for item in items[: max_tracks - offset]:
                yield to_saved_track(item)
                yielded += 1
            offset += 50
        log(f"Fetched {yielded} liked songs.", LogLevel.INFO)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _fetch_artists_batch(self, batch: list[str]) -> dict[str, Any]:
        return self.client.artists(batch)  # type: ignore[no-any-return]

    async def get_artists(self, artist_ids: list[str]) -> list[SpotifyArtist]:
        unique_ids = sorted(set(artist_ids))
        all_artists: list[SpotifyArtist] = []

        log(f"Fetching {len(unique_ids)} unique artists...", LogLevel.INFO)

        for batch in batched(unique_ids, 50):
            response = await asyncio.to_thread(self._fetch_artists_batch, list(batch))
            for artist in response.get("artists", []):
                if not artist:
                    continue  # pragma: no cover
                all_artists.append(to_artist(artist))

        log(f"Retrieved {len(all_artists)} artists.", LogLevel.INFO)
        return all_artists
