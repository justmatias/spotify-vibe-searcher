from chromadb.utils.embedding_functions import (
    OllamaEmbeddingFunction as _OllamaEmbeddingFunction,
)

from vibra.utils import Settings


class OllamaEmbeddingFunction(_OllamaEmbeddingFunction):
    def __init__(self, model_name: str = Settings.EMBEDDING_MODEL) -> None:
        super().__init__(model_name=model_name)
