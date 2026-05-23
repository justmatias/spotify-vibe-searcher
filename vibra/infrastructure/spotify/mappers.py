from typing import Any

from vibra.domain import OAuthToken, SavedTrack, SpotifyArtist, SpotifyUser


def to_user(payload: dict[str, Any]) -> SpotifyUser:
    """Create SpotifyUser from Spotify API response."""
    images = payload.get("images", [])
    image_url = images[0]["url"] if images else None
    return SpotifyUser(
        id=payload["id"],
        display_name=payload.get("display_name", payload["id"]),
        email=payload.get("email"),
        country=payload.get("country"),
        product=payload.get("product"),
        image_url=image_url,
        followers=payload.get("followers", {}).get("total", 0),
    )


def to_artist(payload: dict[str, Any]) -> SpotifyArtist:
    return SpotifyArtist(**payload)


def to_saved_track(payload: dict[str, Any]) -> SavedTrack:
    return SavedTrack(**payload)


def to_token(payload: dict[str, Any]) -> OAuthToken:
    return OAuthToken(**payload)
