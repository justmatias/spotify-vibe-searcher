import asyncio
from functools import cached_property

import stamina
from pydantic import BaseModel
from spotipy.oauth2 import CacheFileHandler, SpotifyOAuth, SpotifyOauthError

from vibra.domain import OAuthToken
from vibra.utils import LogLevel, Settings, log

from .config import RETRY_ON
from .mappers import to_token


class SpotifyAuthManager(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    @cached_property
    def oauth(self) -> SpotifyOAuth:
        return SpotifyOAuth(
            client_id=Settings.SPOTIFY_CLIENT_ID,
            client_secret=Settings.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Settings.SPOTIFY_REDIRECT_URI,
            scope=Settings.SPOTIFY_SCOPES,
            cache_handler=CacheFileHandler(
                cache_path=str(Settings.CACHE_PATH / ".spotify_cache")
            ),
            show_dialog=True,
        )

    def get_auth_url(self) -> str:
        return self.oauth.get_authorize_url()  # type: ignore[no-any-return]

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _exchange_code_sync(self, code: str) -> OAuthToken | None:
        try:
            self.clear_cache()
            token_info = self.oauth.get_access_token(code, as_dict=True)
            return to_token(token_info)
        except SpotifyOauthError as e:
            log(f"Failed to get access token: {e}", LogLevel.WARNING)
            return None

    async def exchange_code(self, code: str) -> OAuthToken | None:
        return await asyncio.to_thread(self._exchange_code_sync, code)

    async def cached_token(self) -> OAuthToken | None:
        def _get() -> OAuthToken | None:
            token_info = self.oauth.cache_handler.get_cached_token()
            if not token_info or "expires_at" not in token_info:
                return None
            token_info = self.oauth.validate_token(token_info)
            return to_token(token_info)

        return await asyncio.to_thread(_get)

    @stamina.retry(on=RETRY_ON, attempts=3)
    def _refresh_sync(self, refresh_token: str) -> OAuthToken | None:
        try:
            token_info = self.oauth.refresh_access_token(refresh_token)
            return to_token(token_info)
        except SpotifyOauthError as e:
            log(f"Failed to refresh token: {e}", LogLevel.WARNING)
            return None

    async def refresh(self, refresh_token: str) -> OAuthToken | None:
        return await asyncio.to_thread(self._refresh_sync, refresh_token)

    def clear_cache(self) -> None:  # pylint: disable=no-self-use
        cache_path = Settings.CACHE_PATH / ".spotify_cache"
        if cache_path.exists():
            cache_path.unlink()
