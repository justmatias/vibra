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

    # Factories (one instance per user)
    library_client = providers.Factory(
        SpotifyClient,
        access_token=config.spotify.access_token,
    )

    # Singletons
    spotify_auth_manager = providers.Singleton(SpotifyAuthManager)
    lyrics_client = providers.Singleton(GeniusClient)
    text_generator = providers.Singleton(LLMClient)
    vector_store = providers.Singleton(VectorDBRepository)
