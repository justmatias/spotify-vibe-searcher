from polyfactory.factories.pydantic_factory import ModelFactory

from spotify_rag.domain.track import (
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyTrack,
)


def test_spotify_album_cover_image(
    album_with_image: SpotifyAlbum,
    spotify_album_factory: ModelFactory[SpotifyAlbum],
) -> None:
    assert album_with_image.cover_image == "http://example.com/image.jpg"
    album_empty = spotify_album_factory.build(images=[])
    assert album_empty.cover_image is None


def test_spotify_track_properties(
    track_with_artists: SpotifyTrack,
    track_without_spotify_url: SpotifyTrack,
) -> None:
    assert track_with_artists.artist_names == "Artist One, Artist Two"
    assert track_with_artists.spotify_url == "http://spotify.com/track/123"
    assert track_without_spotify_url.spotify_url is None


def test_spotify_artist_from_api_response() -> None:
    data = {
        "id": "123",
        "name": "Test Artist",
        "uri": "spotify:artist:123",
        "href": "http://api.spotify.com",
        "external_urls": {},
    }
    artist = SpotifyArtist.from_api_response(data)
    assert artist.id_ == "123"
    assert artist.name == "Test Artist"


def test_saved_track_from_api_response(
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> None:
    track_data = spotify_track_factory.build().model_dump(by_alias=True)
    data = {"added_at": "2023-01-01T00:00:00", "track": track_data}
    saved_track = SavedTrack.from_api_response(data)
    assert saved_track.added_at.year == 2023
    assert saved_track.track.id_ == track_data["id"]
