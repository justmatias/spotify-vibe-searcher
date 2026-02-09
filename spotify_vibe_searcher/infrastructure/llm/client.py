from functools import cached_property

import stamina
from openai import OpenAI
from pydantic import BaseModel

from spotify_vibe_searcher.utils import LogLevel, Settings, log

from .config import RETRY_ON


class LLMClient(BaseModel):
    @cached_property
    def client(self) -> OpenAI:
        return OpenAI(base_url=Settings.LLM_BASE_URL, api_key=Settings.LLM_API_KEY)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=Settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=Settings.TEMPERATURE,
            )
            return response.choices[0].message.content.strip()  # type: ignore[no-any-return]
        except RETRY_ON:  # pragma: no cover
            raise
        except Exception as e:
            log(f"LLM generation failed: {e}", LogLevel.ERROR)
            raise RuntimeError(f"Failed to generate text: {e}") from e
