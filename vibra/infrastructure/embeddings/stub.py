"""Deterministic stub embedding function — no Ollama required."""

import hashlib

from chromadb import EmbeddingFunction, Embeddings


class StubEmbeddingFunction(EmbeddingFunction[list[str]]):
    """Deterministic embeddings derived from SHA-256 of text content.

    Produces all-positive unit vectors so cosine distances stay in [0, 1].
    Suitable for tests and local development without Ollama.
    """

    DIM = 768

    def __init__(self) -> None:
        pass

    @staticmethod
    def name() -> str:
        return "stub"

    def get_config(self) -> dict[str, object]:
        return {}

    @staticmethod
    def build_from_config(config: dict[str, object]) -> "StubEmbeddingFunction":
        return StubEmbeddingFunction()

    def __call__(self, input: list[str]) -> Embeddings:
        return [self._embed(text) for text in input]

    @staticmethod
    def _embed(text: str) -> list[float]:
        digest = hashlib.sha256(text.encode()).digest()  # 32 bytes
        tiled = (digest * (StubEmbeddingFunction.DIM // 32 + 1))[: StubEmbeddingFunction.DIM]
        return [b / 255.0 for b in tiled]
