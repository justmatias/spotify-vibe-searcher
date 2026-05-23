from pydantic import BaseModel, ConfigDict, Field

from .track import SavedTrack


class SyncProgress(BaseModel):
    current: int
    total: int
    song_title: str
    artist_name: str

    model_config = ConfigDict(frozen=True)


class EnrichedTrack(BaseModel):
    track: SavedTrack
    lyrics: str
    vibe_description: str | None = Field(
        default=None,
        description="AI-generated vibe description",
    )
    model_config = ConfigDict(frozen=True)

    @property
    def saved_track(self) -> SavedTrack:
        return self.track

    @property
    def track_id(self) -> str:
        return self.saved_track.track_id

    @property
    def has_lyrics(self) -> bool:
        return bool(self.lyrics)
