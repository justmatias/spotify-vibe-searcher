# pylint: disable=invalid-name

import os
from pathlib import Path
from typing import Literal

from dotenv import dotenv_values, load_dotenv
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import LogLevel, log


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    ENVIRONMENT: Literal["testing", "production"] = "testing"

    # Spotify API Configuration
    SPOTIFY_CLIENT_ID: str = Field(description="Spotify API Client ID")
    SPOTIFY_CLIENT_SECRET: str = Field(
        description="Spotify API Client Secret",
    )
    SPOTIFY_REDIRECT_URI: str = Field(
        description="OAuth redirect URI registered",
        default="http://127.0.0.1:8501/callback",
    )
    SPOTIFY_SCOPES: str = Field(
        default="user-library-read user-read-private user-read-email",
        description="Space-separated list of Spotify API scopes",
    )

    # Genius API Configuration
    GENIUS_API_KEY: str = Field(description="Genius API Key")

    # Application Paths
    DATA_DIR: Path = Field(
        default=Path("./data"),
        description="Directory for storing application data",
    )

    CHROMADB_COLLECTION: str = Field(
        default="tracks",
        description="ChromaDB collection name",
    )

    EMBEDDING_MODEL: str = Field(
        default="nomic-embed-text:v1.5",
        description="Embedding model to use",
    )
    LLM_BASE_URL: str = Field(
        default="http://localhost:11434/v1",
        description="LLM API base URL",
    )
    LLM_MODEL: str = Field(
        default="llama3.2:3b",
        description="LLM model for semantic analysis",
    )
    LLM_API_KEY: str = Field(
        default="ollama",  # Ollama doesn't need a real API key
        description="LLM API key",
    )
    TEMPERATURE: float = Field(
        default=0.7,
        description="Temperature for LLM generation",
    )
    LLM_CONCURRENCY_LIMIT: int = Field(
        default=3,
        description="Maximum number of concurrent LLM requests during library sync",
    )

    @property
    def CHROMADB_PATH(self) -> Path:
        """Path to ChromaDB persistent storage."""
        return self.DATA_DIR / "chromadb"

    @property
    def CACHE_PATH(self) -> Path:
        """Path to cache directory."""
        return self.DATA_DIR / "cache"


class AppSettingsFactory(ModelFactory[AppSettings]):
    __model__ = AppSettings
    __use_defaults__ = True


def get_settings() -> AppSettings:
    load_dotenv(override=True)
    environment = os.getenv("ENVIRONMENT", "testing").lower()

    def load_test_settings() -> AppSettings:
        log("Loading test settings...")
        overrides = {k: v for k, v in dotenv_values(".env").items() if v}
        log(
            f"Overriding factory values from .env: {list(overrides.keys())}",
            LogLevel.WARNING,
        )
        return AppSettingsFactory.build(**overrides)  # type: ignore[arg-type]

    def load_production_settings() -> AppSettings:  # pragma: no cover
        log("Loading production settings...")
        try:
            return AppSettings()  # type: ignore[call-arg]
        except ValidationError as e:
            log(f"Error loading production settings: {e}", LogLevel.ERROR)
            raise

    loaders = {
        "production": load_production_settings,
        "testing": load_test_settings,
    }
    return loaders[environment]()


Settings = get_settings()
