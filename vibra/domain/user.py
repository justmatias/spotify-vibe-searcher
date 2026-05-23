from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
    refresh_token: str
    expires_at: datetime
    scope: str
    token_type: str

    model_config = ConfigDict(frozen=True)
