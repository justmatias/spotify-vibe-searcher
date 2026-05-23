"""Embedding function implementations."""

from .ollama import OllamaEmbeddingFunction
from .stub import StubEmbeddingFunction

__all__ = ["OllamaEmbeddingFunction", "StubEmbeddingFunction"]
