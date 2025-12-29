import pytest

from spotify_rag.infrastructure.spotify import SpotifyClient
from tests.helpers.auth import get_spotify_token


@pytest.fixture
def spotify_client() -> SpotifyClient:
    # Use real token from auth helper for recording, fallback to test_token for replay
    # if auth helper returns None (no cache)
    token = get_spotify_token() or "test_token"
    return SpotifyClient(access_token=token)


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
