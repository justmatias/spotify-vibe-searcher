from vibra.infrastructure import GeniusClient, SpotifyClient
from vibra.domain.ports import (
    AuthProvider,
    LLMProvider,
    LyricsProvider,
    MusicLibrary,
    VectorStore,
)
from vibra.injections import Container, container
from vibra.services import LibrarySyncService


def test_container_initialization() -> None:
    container = Container()
    assert container


def test_singleton_container_exists() -> None:
    assert container


def test_spotify_client_creation() -> None:
    container.infrastructure.config.spotify.access_token.from_value("test_token")

    client = container.infrastructure.spotify_client()
    assert isinstance(client, SpotifyClient)
    assert isinstance(client, MusicLibrary)


def test_genius_client_creation() -> None:
    client = container.infrastructure.genius_client()
    assert isinstance(client, GeniusClient)
    assert isinstance(client, LyricsProvider)


def test_llm_client_satisfies_protocol() -> None:
    client = container.infrastructure.llm_client()
    assert isinstance(client, LLMProvider)


def test_vectordb_repository_satisfies_protocol() -> None:
    repo = container.infrastructure.vectordb_repository()
    assert isinstance(repo, VectorStore)


def test_auth_manager_satisfies_protocol() -> None:
    manager = container.infrastructure.spotify_auth_manager()
    assert isinstance(manager, AuthProvider)


def test_library_sync_service_creation() -> None:
    container.infrastructure.config.spotify.access_token.from_value("test_token")

    service = container.services.library_sync_service()
    assert isinstance(service, LibrarySyncService)
