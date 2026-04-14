"""Service dependency providers."""

from dependency_injector import containers, providers

from vibra.services import (
    LibrarySyncService,
    SearchService,
    TrackAnalysisService,
)


class ServicesContainer(containers.DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()

    track_analysis_service = providers.Factory(
        TrackAnalysisService,
        llm_client=infrastructure.llm_client,
    )

    search_service = providers.Factory(
        SearchService,
        vectordb_repository=infrastructure.vectordb_repository,
        llm_client=infrastructure.llm_client,
    )

    library_sync_service = providers.Factory(
        LibrarySyncService,
        spotify_client=infrastructure.spotify_client,
        genius_client=infrastructure.genius_client,
        track_analysis_service=track_analysis_service,
        vectordb_repository=infrastructure.vectordb_repository,
    )
