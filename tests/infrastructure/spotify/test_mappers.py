"""Pure unit tests for spotify mappers — no I/O, no cassettes."""

from typing import Any

from vibra.domain import OAuthToken, SavedTrack, SpotifyArtist, SpotifyUser
from vibra.infrastructure.spotify.mappers import (
    to_artist,
    to_saved_track,
    to_token,
    to_user,
)


def test_to_user_maps_id_and_display_name() -> None:
    payload = {
        "id": "user_123",
        "display_name": "Matias",
        "email": "m@example.com",
        "country": "AR",
        "product": "premium",
        "images": [{"url": "https://img.example.com/avatar.jpg"}],
        "followers": {"total": 42},
    }

    user = to_user(payload)

    assert isinstance(user, SpotifyUser)
    assert user.id == "user_123"
    assert user.display_name == "Matias"
    assert user.email == "m@example.com"
    assert user.image_url == "https://img.example.com/avatar.jpg"
    assert user.followers == 42


def test_to_user_handles_missing_optional_fields() -> None:
    user = to_user({"id": "bare_user"})

    assert user.id == "bare_user"
    assert user.display_name == "bare_user"
    assert user.email is None
    assert user.image_url is None
    assert user.followers == 0


def test_to_artist_maps_fields(spotify_artist_payload: dict[str, Any]) -> None:
    artist = to_artist(spotify_artist_payload)

    assert isinstance(artist, SpotifyArtist)
    assert artist.id_ == "artist_123"
    assert artist.name == "Test Artist"
    assert artist.genres == ["rock", "indie"]


def test_to_artist_defaults_empty_genres(spotify_artist_payload: dict[str, Any]) -> None:
    payload = {**spotify_artist_payload, "genres": []}
    artist = to_artist(payload)

    assert artist.genres == []


def test_to_saved_track_maps_nested_structure(
    spotify_saved_track_payload: dict[str, Any],
) -> None:
    saved_track = to_saved_track(spotify_saved_track_payload)

    assert isinstance(saved_track, SavedTrack)
    assert saved_track.track.id_ == "track_123"
    assert saved_track.track.name == "Test Track"
    assert saved_track.track.album.name == "Test Album"
    assert saved_track.track.artists[0].id_ == "artist_123"


def test_to_saved_track_album_cover_image(
    spotify_saved_track_payload: dict[str, Any],
) -> None:
    saved_track = to_saved_track(spotify_saved_track_payload)

    assert saved_track.track.album.cover_image == "https://img.example.com/cover.jpg"


def test_to_token_maps_all_fields(spotify_token_payload: dict[str, Any]) -> None:
    token = to_token(spotify_token_payload)

    assert isinstance(token, OAuthToken)
    assert token.access_token == "access_abc"
    assert token.refresh_token == "refresh_xyz"
    assert token.scope == "user-library-read"
    assert token.token_type == "Bearer"
