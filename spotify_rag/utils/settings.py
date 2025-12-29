# pylint: disable=invalid-name
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
    SPOTIFY_CLIENT_ID: str = Field(
        description="Spotify API Client ID",
        default="TEST_SPOTIFY_CLIENT_ID",
    )
    SPOTIFY_CLIENT_SECRET: str = Field(
        description="Spotify API Client Secret",
        default="TEST_SPOTIFY_CLIENT_SECRET",
    )
    SPOTIFY_REDIRECT_URI: str = Field(
        description="OAuth redirect URI registered",
        default="TEST_SPOTIFY_REDIRECT_URI",
    )
    SPOTIFY_SCOPES: str = Field(
        default="user-library-read user-read-private user-read-email",
        description="Space-separated list of Spotify API scopes",
    )

    # Genius API Configuration
    GENIUS_API_KEY: str = Field(
        description="Genius API Key",
        default="TEST_GENIUS_API_KEY",
    )

    # Application Paths
    DATA_DIR: Path = Field(
        default=Path("./data"),
        description="Directory for storing application data",
    )

    @property
    def CHROMADB_PATH(self) -> Path:
        """Path to ChromaDB persistent storage."""
        return self.DATA_DIR / "chromadb"

    @property
    def CACHE_PATH(self) -> Path:
        """Path to cache directory."""
        return self.DATA_DIR / "cache"


@lru_cache
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()


Settings = get_settings()
