"""Domain models for library sync operations."""

from pydantic import BaseModel

from .track import SavedTrack


class SyncProgress(BaseModel):
    """Progress update for library sync."""

    current: int
    total: int
    song_title: str
    artist_name: str


class EnrichedTrack(BaseModel):
    """Track enriched with lyrics."""

    track: SavedTrack
    lyrics: str
    has_lyrics: bool
