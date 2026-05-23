import pytest

from vibra.domain import SavedTrack, SpotifyArtist, SpotifyUser
from vibra.infrastructure.spotify import SpotifyClient


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_current_user(spotify_client: SpotifyClient) -> None:
    user = await spotify_client.current_user()
    assert isinstance(user, SpotifyUser)


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_all_liked_songs(spotify_client: SpotifyClient) -> None:
    tracks = []
    async for track in spotify_client.read_liked_songs(max_tracks=10):
        tracks.append(track)
    assert all(isinstance(track, SavedTrack) for track in tracks)
    assert len(tracks) <= 10


@pytest.mark.asyncio
@pytest.mark.vcr
async def test_get_artists(spotify_client: SpotifyClient, artist_ids: list[str]) -> None:
    artists = await spotify_client.get_artists(artist_ids)
    assert len(artists) == len(artist_ids)
    assert all(isinstance(artist, SpotifyArtist) for artist in artists)
