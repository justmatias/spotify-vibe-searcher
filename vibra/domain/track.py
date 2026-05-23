"""Domain models for Spotify tracks and albums."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SpotifyImage(BaseModel):
    url: str
    height: int | None = None
    width: int | None = None
    model_config = ConfigDict(frozen=True)


class SpotifyArtist(BaseModel):
    id_: str = Field(alias="id")
    name: str
    uri: str
    href: str
    external_urls: dict[str, str]
    genres: list[str] = Field(default_factory=list)
    model_config = ConfigDict(frozen=True)

    @property
    def genre_names(self) -> str:
        return ", ".join(genre for genre in self.genres)


class SpotifyAlbum(BaseModel):
    id_: str = Field(alias="id")
    name: str
    album_type: str
    images: list[SpotifyImage] = Field(default_factory=list)
    release_date: str
    total_tracks: int
    uri: str
    external_urls: dict[str, str]

    @property
    def cover_image(self) -> str | None:
        return self.images[0].url if self.images else None

    model_config = ConfigDict(frozen=True)


class SpotifyTrack(BaseModel):
    id_: str = Field(alias="id")
    name: str
    artists: list[SpotifyArtist] = Field(default_factory=list)
    album: SpotifyAlbum
    duration_ms: int
    explicit: bool
    popularity: int
    uri: str
    external_urls: dict[str, str]
    preview_url: str | None = None
    is_playable: bool = True
    model_config = ConfigDict(frozen=True)

    @property
    def artist_names(self) -> str:
        return ", ".join(artist.name for artist in self.artists)

    @property
    def spotify_url(self) -> str:
        return self.external_urls.get("spotify", "")

    @property
    def all_genre_names(self) -> str:
        """Get unique genre names from all artists as a comma-separated string."""
        unique_genres = {genre for artist in self.artists for genre in artist.genres}
        return ", ".join(unique_genres)


class SavedTrack(BaseModel):
    added_at: datetime
    track: SpotifyTrack
    model_config = ConfigDict(frozen=True)

    @property
    def track_id(self) -> str:
        return self.track.id_


class IndexedTrack(BaseModel):
    id: str
    track_name: str
    artist_names: str
    album_name: str
    vibe_description: str
    popularity: int
    spotify_url: str
    model_config = ConfigDict(frozen=True)
