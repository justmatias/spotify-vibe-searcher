import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from spotify_rag.domain.track import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyImage,
    SpotifyTrack,
)


@pytest.fixture
def album_with_image(
    spotify_image_factory: ModelFactory[SpotifyImage],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
) -> SpotifyAlbum:
    image = spotify_image_factory.build(url="http://example.com/image.jpg")
    return spotify_album_factory.build(images=[image])


@pytest.fixture
def track_with_artists(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    artist1 = spotify_artist_factory.build(name="Artist One")
    artist2 = spotify_artist_factory.build(name="Artist Two")
    album = spotify_album_factory.build()

    return spotify_track_factory.build(
        artists=[artist1, artist2],
        album=album,
        external_urls={"spotify": "http://spotify.com/track/123"},
    )


@pytest.fixture
def track_without_spotify_url(
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    return spotify_track_factory.build(external_urls={})
