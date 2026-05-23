"""Infrastructure dependency providers."""

from dependency_injector import containers, providers

from vibra.infrastructure import (
    GeniusClient,
    LLMClient,
    SpotifyAuthManager,
    SpotifyClient,
    VectorDBRepository,
)


class InfrastructureContainer(containers.DeclarativeContainer):
    """Container for infrastructure layer dependencies."""

    # Factory — caller passes access_token at call time:
    # container.infrastructure.spotify_client(access_token=token.access_token)
    spotify_client = providers.Factory(SpotifyClient)

    # Singletons
    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    genius_client = providers.Singleton(GeniusClient)
    llm_client = providers.Singleton(LLMClient)
    vectordb_repository = providers.Singleton(VectorDBRepository)
