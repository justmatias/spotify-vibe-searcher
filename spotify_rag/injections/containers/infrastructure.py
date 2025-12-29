"""Infrastructure dependency providers."""

from dependency_injector import containers, providers

from spotify_rag.infrastructure import GeniusClient, SpotifyClient


class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    # Spotify Client - Factory (new instance per request with access token)
    spotify_client = providers.Factory(
        SpotifyClient,
        access_token=config.spotify.access_token,
    )

    # Genius Client - Singleton (shared instance, no auth needed)
    genius_client = providers.Singleton(GeniusClient)
