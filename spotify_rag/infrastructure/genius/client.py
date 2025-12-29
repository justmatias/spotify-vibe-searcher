"""Genius API client wrapper using lyricsgenius."""

import contextlib
import re

from lyricsgenius import Genius
from pydantic import BaseModel

from spotify_rag.utils import Settings


class GeniusClient(BaseModel):
    """Client for interacting with the Genius API to fetch lyrics."""

    @property
    def client(self) -> Genius:
        return Genius(
            Settings.GENIUS_API_KEY,
            verbose=False,
            remove_section_headers=True,
        )

    def _sanitize_title(self, title: str) -> str:  # pylint: disable=no-self-use
        """Clean the title to improve search hit rate.

        Removes:
        - " - Remastered..."
        - " - Live..."
        - Content in parentheses that indicates remastering or live versions.
        """
        # Remove specific suffixes
        clean_title = re.sub(r" - Remastered.*", "", title, flags=re.IGNORECASE)
        clean_title = re.sub(r" - Live.*", "", clean_title, flags=re.IGNORECASE)

        # Remove (Remastered...) or (Live...)
        clean_title = re.sub(
            r"\(.*Remastered.*\)", "", clean_title, flags=re.IGNORECASE
        )
        clean_title = re.sub(r"\(.*Live.*\)", "", clean_title, flags=re.IGNORECASE)

        # Remove [Remastered...] or [Live...]
        clean_title = re.sub(
            r"\[.*Remastered.*\]", "", clean_title, flags=re.IGNORECASE
        )
        clean_title = re.sub(r"\[.*Live.*\]", "", clean_title, flags=re.IGNORECASE)

        return clean_title.strip()

    def search_song(self, title: str, artist: str) -> str:
        clean_title = self._sanitize_title(title)
        lyrics = ""
        with contextlib.suppress(Exception):
            song = self.client.search_song(clean_title, artist)
            if song and song.lyrics:
                lyrics = song.lyrics
        return lyrics
