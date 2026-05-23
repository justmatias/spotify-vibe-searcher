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

    # Used by library_sync_service (Phase 3 will remove this config dependency)
    config = providers.Configuration()

    # Factory — callers may override access_token at call time:
    # container.infrastructure.spotify_client(access_token=token.access_token)
    spotify_client = providers.Factory(
        SpotifyClient,
        access_token=config.spotify.access_token,
    )

    # Singletons
    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    genius_client = providers.Singleton(GeniusClient)
    llm_client = providers.Singleton(LLMClient)
    vectordb_repository = providers.Singleton(VectorDBRepository)
