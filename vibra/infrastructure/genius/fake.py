"""In-process Genius fake for tests and local dev without the Genius API."""

from dataclasses import dataclass


@dataclass
class FakeGeniusClient:
    """Implements LyricsProvider without hitting the Genius API."""

    lyrics: str = "Fake lyrics content for testing."

    async def fetch(self, *, title: str, artist: str) -> str:  # pylint: disable=unused-argument
        return self.lyrics
