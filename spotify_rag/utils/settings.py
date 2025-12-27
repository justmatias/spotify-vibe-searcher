"""Application configuration using Pydantic BaseSettings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Spotify API Configuration
    spotify_client_id: str = Field(description="Spotify API Client ID")
    spotify_client_secret: str = Field(description="Spotify API Client Secret")
    spotify_redirect_uri: str = Field(description="OAuth redirect URI registered")

    # Spotify API Scopes
    spotify_scopes: str = Field(
        default="user-library-read user-read-private user-read-email",
        description="Space-separated list of Spotify API scopes",
    )

    # Application Paths
    data_dir: Path = Field(
        default=Path("./data"),
        description="Directory for storing application data",
    )

    @property
    def chromadb_path(self) -> Path:
        """Path to ChromaDB persistent storage."""
        return self.data_dir / "chromadb"

    @property
    def cache_path(self) -> Path:
        """Path to cache directory."""
        return self.data_dir / "cache"


@lru_cache
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()


Settings = get_settings()
