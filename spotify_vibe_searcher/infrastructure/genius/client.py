from functools import cached_property

import stamina
from lyricsgenius import Genius
from pydantic import BaseModel
from requests.exceptions import RequestException

from spotify_vibe_searcher.utils import LogLevel, Settings, log

from .config import TITLE_CLEANUP_PATTERN


class GeniusClient(BaseModel):
    """Client for interacting with the Genius API to fetch lyrics."""

    @cached_property
    def client(self) -> Genius:
        return Genius(
            Settings.GENIUS_API_KEY,
            verbose=False,
            remove_section_headers=True,
        )

    def search_song(self, title: str, artist: str) -> str:
        """Search for song lyrics with sanitization and error handling."""
        clean_title = self._sanitize_title(title)
        log(
            f"Searching lyrics for: '{clean_title}' by '{artist}' (Original: '{title}')",
            LogLevel.DEBUG,
        )

        try:
            lyrics = self._fetch_lyrics(clean_title, artist)
        except Exception as e:
            log(
                f"Failed to fetch lyrics for '{clean_title}' after retries: {e}",
                LogLevel.WARNING,
            )
            return ""
        return lyrics or ""

    @stamina.retry(
        on=(RequestException, TimeoutError, ConnectionError),
        attempts=3,
        wait_initial=2.0,
        wait_max=10.0,
    )
    def _fetch_lyrics(self, clean_title: str, artist: str) -> str | None:
        """Fetch lyrics from Genius API with retry logic."""
        song = self.client.search_song(clean_title, artist)
        if song and song.lyrics:
            log(f"Found lyrics for: {clean_title} - {artist}", LogLevel.INFO)
            return song.lyrics
        return None

    def _sanitize_title(self, title: str) -> str:  # pylint: disable=no-self-use
        return TITLE_CLEANUP_PATTERN.sub("", title).strip()
