from typing import Any

import pytest


@pytest.fixture
def spotify_artist_payload() -> dict[str, Any]:
    return {
        "id": "artist_123",
        "name": "Test Artist",
        "uri": "spotify:artist:artist_123",
        "href": "https://api.spotify.com/v1/artists/artist_123",
        "external_urls": {"spotify": "https://open.spotify.com/artist/artist_123"},
        "genres": ["rock", "indie"],
    }


@pytest.fixture
def spotify_track_payload(spotify_artist_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": "track_123",
        "name": "Test Track",
        "artists": [spotify_artist_payload],
        "album": {
            "id": "album_123",
            "name": "Test Album",
            "album_type": "album",
            "images": [{"url": "https://img.example.com/cover.jpg", "height": 640, "width": 640}],
            "release_date": "2020-01-01",
            "total_tracks": 12,
            "uri": "spotify:album:album_123",
            "external_urls": {"spotify": "https://open.spotify.com/album/album_123"},
        },
        "duration_ms": 240000,
        "explicit": False,
        "popularity": 78,
        "uri": "spotify:track:track_123",
        "external_urls": {"spotify": "https://open.spotify.com/track/track_123"},
    }


@pytest.fixture
def spotify_saved_track_payload(spotify_track_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "added_at": "2023-06-15T12:00:00Z",
        "track": spotify_track_payload,
    }


@pytest.fixture
def spotify_token_payload() -> dict[str, Any]:
    return {
        "access_token": "access_abc",
        "refresh_token": "refresh_xyz",
        "expires_at": 9999999999.0,
        "scope": "user-library-read",
        "token_type": "Bearer",
    }
