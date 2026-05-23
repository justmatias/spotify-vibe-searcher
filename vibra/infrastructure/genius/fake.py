from dataclasses import dataclass


@dataclass
class FakeGeniusClient:
    lyrics: str = "Fake lyrics content for testing."

    async def fetch(self, *, title: str, artist: str) -> str:  # pylint: disable=unused-argument
        return self.lyrics
