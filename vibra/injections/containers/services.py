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
        text_generator=infrastructure.text_generator,
    )

    search_service = providers.Factory(
        SearchService,
        vector_store=infrastructure.vector_store,
        text_generator=infrastructure.text_generator,
    )

    library_sync_service = providers.Factory(
        LibrarySyncService,
        library=infrastructure.library_client,
        lyrics_provider=infrastructure.lyrics_client,
        track_analysis_service=track_analysis_service,
        vector_store=infrastructure.vector_store,
    )
