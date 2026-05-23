"""Infrastructure dependency providers."""

import chromadb
from dependency_injector import containers, providers

from vibra.infrastructure import (
    GeniusClient,
    LLMClient,
    OllamaEmbeddingFunction,
    SpotifyAuthManager,
    SpotifyClient,
    VectorDBRepository,
)
from vibra.utils import Settings


class InfrastructureContainer(containers.DeclarativeContainer):
    """Container for infrastructure layer dependencies."""

    # Spotify access token is supplied per-request at call time:
    #   container.infrastructure.spotify_client(access_token=token.access_token)
    config = providers.Configuration()

    spotify_client = providers.Factory(
        SpotifyClient,
        access_token=config.spotify.access_token,
    )

    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    genius_client = providers.Singleton(GeniusClient)
    llm_client = providers.Singleton(LLMClient)

    _chromadb_client = providers.Singleton(
        chromadb.PersistentClient,
        path=str(Settings.CHROMADB_PATH),
    )
    _embedding_fn = providers.Singleton(
        OllamaEmbeddingFunction,
        model_name=Settings.EMBEDDING_MODEL,
    )
    vectordb_repository = providers.Singleton(
        VectorDBRepository,
        client=_chromadb_client,
        embedding_fn=_embedding_fn,
    )
