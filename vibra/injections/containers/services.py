from dependency_injector import containers, providers

from vibra.services import (
    EnrichmentService,
    IndexingService,
    LibrarySyncService,
    SearchService,
    TrackAnalysisService,
    TrackFetchService,
)


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    track_analysis_service = providers.Factory(
        TrackAnalysisService,
        llm_client=infrastructure.llm_client,
    )

    track_fetch_service = providers.Factory(
        TrackFetchService,
        music_library=infrastructure.spotify_client,
    )

    enrichment_service = providers.Factory(
        EnrichmentService,
        lyrics=infrastructure.genius_client,
        analyzer=track_analysis_service,
    )

    indexing_service = providers.Factory(
        IndexingService,
        store=infrastructure.vectordb_repository,
    )

    library_sync_service = providers.Factory(
        LibrarySyncService,
        track_fetch=track_fetch_service,
        enrichment=enrichment_service,
        indexing=indexing_service,
    )

    search_service = providers.Factory(
        SearchService,
        vectordb_repository=infrastructure.vectordb_repository,
        llm_client=infrastructure.llm_client,
    )
