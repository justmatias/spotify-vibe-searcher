from dataclasses import dataclass


@dataclass
class FakeLLMClient:
    response: str = "Generated vibe description for testing."

    async def generate(self, prompt: str) -> str:  # pylint: disable=unused-argument
        return self.response
