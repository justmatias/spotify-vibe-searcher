"""Service dependency providers."""

from dependency_injector import containers, providers

from spotify_rag.services import LibrarySyncService


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    library_sync_service = providers.Factory(
        LibrarySyncService,
        spotify_client=infrastructure.spotify_client,
        genius_client=infrastructure.genius_client,
    )
