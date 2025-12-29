import contextlib
from dataclasses import dataclass
from typing import Any

from spotipy.oauth2 import CacheFileHandler, SpotifyOAuth

from spotify_rag.utils import Settings


@dataclass
class SpotifyAuthManager:
    _oauth: SpotifyOAuth | None = None

    @property
    def oauth(self) -> SpotifyOAuth:
        """Get or create the SpotifyOAuth instance."""
        if self._oauth is None:
            cache_handler = CacheFileHandler(
                cache_path=str(Settings.CACHE_PATH / ".spotify_cache")
            )
            self._oauth = SpotifyOAuth(
                client_id=Settings.SPOTIFY_CLIENT_ID,
                client_secret=Settings.SPOTIFY_CLIENT_SECRET,
                redirect_uri=Settings.SPOTIFY_REDIRECT_URI,
                scope=Settings.SPOTIFY_SCOPES,
                cache_handler=cache_handler,
                show_dialog=True,
            )
        return self._oauth

    def get_auth_url(self) -> str:
        return self.oauth.get_authorize_url()  # type: ignore[no-any-return]

    def get_access_token(self, code: str) -> dict[str, Any] | None:
        with contextlib.suppress(Exception):
            return self.oauth.get_access_token(code, as_dict=True)  # type: ignore[no-any-return]
        return None

    def get_cached_token(self) -> dict[str, Any] | None:
        token_info = self.oauth.cache_handler.get_cached_token()
        if not token_info:
            return None
        return self.oauth.validate_token(token_info)  # type: ignore[no-any-return]

    def refresh_token(self, refresh_token: str) -> dict[str, Any] | None:
        with contextlib.suppress(Exception):
            return self.oauth.refresh_access_token(refresh_token)  # type: ignore[no-any-return]
        return None
