"""In-process LLM fake for tests and local dev without Ollama."""

from dataclasses import dataclass


@dataclass
class FakeLLMClient:
    """Implements LLMProvider without a running Ollama instance."""

    response: str = "Generated vibe description for testing."

    async def generate(self, prompt: str) -> str:  # pylint: disable=unused-argument
        return self.response
