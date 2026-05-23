from pydantic import BaseModel, ConfigDict

from vibra.domain import MusicLibrary, SavedTrack, SpotifyArtist
from vibra.utils import LogLevel, log


class TrackFetchService(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    music_library: MusicLibrary

    async def fetch(self, limit: int) -> list[SavedTrack]:
        log(f"Fetching up to {limit} liked songs...", LogLevel.INFO)
        tracks: list[SavedTrack] = []
        async for saved_track in self.music_library.read_liked_songs(limit):
            tracks.append(saved_track)

        artist_ids = [artist.id_ for st in tracks for artist in st.track.artists]
        artists_with_genres = await self.music_library.get_artists(artist_ids)
        artist_map: dict[str, SpotifyArtist] = {a.id_: a for a in artists_with_genres}

        enriched: list[SavedTrack] = []
        for saved_track in tracks:
            new_artists = [artist_map.get(a.id_, a) for a in saved_track.track.artists]
            new_track = saved_track.track.model_copy(update={"artists": new_artists})
            enriched.append(saved_track.model_copy(update={"track": new_track}))

        log(f"Fetched {len(enriched)} tracks with genre data.", LogLevel.INFO)
        return enriched
