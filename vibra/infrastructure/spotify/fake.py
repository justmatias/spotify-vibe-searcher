from collections.abc import AsyncIterator
from dataclasses import dataclass, field

from vibra.domain import SavedTrack, SpotifyArtist, SpotifyUser


@dataclass
class FakeSpotifyClient:
    tracks: list[SavedTrack] = field(default_factory=list)
    user: SpotifyUser = field(
        default_factory=lambda: SpotifyUser(
            id="fake_user",
            display_name="Fake User",
            email=None,
            country=None,
            product=None,
            image_url=None,
            followers=0,
        )
    )

    async def current_user(self) -> SpotifyUser:
        return self.user

    async def read_liked_songs(self, max_tracks: int) -> AsyncIterator[SavedTrack]:
        for t in self.tracks[:max_tracks]:
            yield t

    async def get_artists(self, ids: list[str]) -> list[SpotifyArtist]:
        artist_map = {a.id_: a for t in self.tracks for a in t.track.artists}
        return [artist_map[id_] for id_ in ids if id_ in artist_map]
