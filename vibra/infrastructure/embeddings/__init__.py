"""Embedding function implementations."""

from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

from .stub import StubEmbeddingFunction

__all__ = ["OllamaEmbeddingFunction", "StubEmbeddingFunction"]
