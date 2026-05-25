from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class SpotifyUser(BaseModel):
    id: str
    display_name: str
    email: str | None
    country: str | None
    product: str | None
    image_url: str | None
    followers: int
    model_config = ConfigDict(frozen=True)


class OAuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_at: float
    refresh_token: str | None = None
    scope: str = ""
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    model_config = ConfigDict(frozen=True)
