from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain.track import (
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
    assert track_without_spotify_url.spotify_url == ""


def test_genre_names_with_multiple_genres(
    artist_with_multiple_genres: SpotifyArtist,
) -> None:
    assert artist_with_multiple_genres.genre_names == "rock, pop, indie"


def test_genre_names_with_single_genre(
    artist_with_single_genre: SpotifyArtist,
) -> None:
    assert artist_with_single_genre.genre_names == "jazz"


def test_genre_names_with_empty_genres(
    artist_with_no_genres: SpotifyArtist,
) -> None:
    assert artist_with_no_genres.genre_names == ""


def test_all_genre_names_from_multiple_artists(
    track_with_multiple_artist_genres: SpotifyTrack,
) -> None:
    genre_names = track_with_multiple_artist_genres.all_genre_names

    assert "rock" in genre_names
    assert "pop" in genre_names
    assert "indie" in genre_names
    assert "alternative" in genre_names


def test_all_genre_names_deduplicates(
    track_with_duplicate_genres: SpotifyTrack,
) -> None:
    genre_names = track_with_duplicate_genres.all_genre_names

    assert genre_names.count("rock") == 1
    assert genre_names.count("indie") == 1


def test_all_genre_names_empty(
    track_with_no_genres: SpotifyTrack,
) -> None:
    assert track_with_no_genres.all_genre_names == ""
