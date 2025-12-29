from typing import Optional

from openai import OpenAI
from pydantic import BaseModel

from spotify_rag.utils import Settings


class LLMClient(BaseModel):
    _client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            self._client = OpenAI(
                base_url=Settings.LLM_BASE_URL,
                api_key="ollama",  # Ollama doesn't need a real API key
            )
        return self._client

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=Settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=Settings.TEMPERATURE,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate text: {e}") from e
