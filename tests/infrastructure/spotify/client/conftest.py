import asyncio

import pytest
from spotipy.oauth2 import SpotifyOauthError

from vibra.infrastructure import SpotifyAuthManager, SpotifyClient


@pytest.fixture
def spotify_token() -> str:
    """Return a cached Spotify access token for cassette recording, or a mock token."""
    try:
        token = asyncio.run(SpotifyAuthManager().cached_token())
        return token.access_token if token else "MOCKED_TOKEN"
    except SpotifyOauthError:
        return "MOCKED_TOKEN"


@pytest.fixture
def spotify_client(spotify_token: str) -> SpotifyClient:
    return SpotifyClient(access_token=spotify_token)


@pytest.fixture(
    params=[
        ["3TVXtAsR1Inumwj472S9r4"],  # Single artist (Drake)
        [
            "3TVXtAsR1Inumwj472S9r4",
            "1Xyo4u8uXC1ZmMpatF05PJ",
        ],  # Multiple artists (Drake, The Weeknd)
    ],
    ids=["single_artist", "multiple_artists"],
)
def artist_ids(request: pytest.FixtureRequest) -> list[str]:
    return request.param  # type: ignore[no-any-return]
