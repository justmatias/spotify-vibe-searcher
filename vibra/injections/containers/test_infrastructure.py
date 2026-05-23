"""Test infrastructure dependency providers using in-memory fakes."""

import uuid

import chromadb
from dependency_injector import containers, providers

from vibra.infrastructure import (
    FakeGeniusClient,
    FakeLLMClient,
    FakeSpotifyClient,
    SpotifyAuthManager,
    StubEmbeddingFunction,
    VectorDBRepository,
)


class TestInfrastructureContainer(containers.DeclarativeContainer):
    """Infrastructure container that wires fakes instead of real external clients.

    All providers are Singletons so that services resolved from the same
    TestContainer instance share the same fake instances and vector store.
    Mutate fake attributes (e.g. spotify_client().tracks = [...]) before
    resolving a service to inject test-specific state.
    """

    __test__ = False  # prevent pytest from collecting this as a test class

    spotify_client = providers.Singleton(FakeSpotifyClient)
    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    genius_client = providers.Singleton(FakeGeniusClient)
    llm_client = providers.Singleton(FakeLLMClient)

    _chromadb_client = providers.Singleton(chromadb.EphemeralClient)
    _embedding_fn = providers.Singleton(StubEmbeddingFunction)
    # EphemeralClient shares global in-memory state, so each container instance
    # needs a unique collection name to keep test data isolated.
    _collection_name = providers.Callable(lambda: str(uuid.uuid4()))

    vectordb_repository = providers.Singleton(
        VectorDBRepository,
        client=_chromadb_client,
        embedding_fn=_embedding_fn,
        collection_name=_collection_name,
    )
