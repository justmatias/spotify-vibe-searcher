import pytest
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from spotify_rag.domain.track import (
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyImage,
    SpotifyTrack,
)


@register_fixture(name="spotify_image_factory")
class SpotifyImageFactory(ModelFactory[SpotifyImage]): ...


@register_fixture(name="spotify_artist_factory")
class SpotifyArtistFactory(ModelFactory[SpotifyArtist]): ...


@register_fixture(name="spotify_album_factory")
class SpotifyAlbumFactory(ModelFactory[SpotifyAlbum]): ...


@register_fixture(name="spotify_track_factory")
class SpotifyTrackFactory(ModelFactory[SpotifyTrack]):
    __random_seed__ = 123


@register_fixture(name="saved_track_factory")
class SavedTrackFactory(ModelFactory[SavedTrack]): ...


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
