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

    config = providers.Configuration()

    # Factories(one instance per user)
    spotify_client = providers.Factory(
        SpotifyClient,
        access_token=config.spotify.access_token,
    )

    # Singletons
    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    genius_client = providers.Singleton(GeniusClient)
    llm_client = providers.Singleton(LLMClient)
    vectordb_repository = providers.Singleton(VectorDBRepository)
