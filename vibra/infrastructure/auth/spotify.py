from functools import cached_property
from typing import Any

import stamina
from pydantic import BaseModel
from spotipy.oauth2 import CacheFileHandler, SpotifyOAuth, SpotifyOauthError

from vibra.infrastructure.spotify.config import RETRY_ON
from vibra.utils import LogLevel, Settings, log


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
    def get_access_token(self, code: str) -> dict[str, Any] | None:
        try:
            return self.oauth.get_access_token(code, as_dict=True)  # type: ignore[no-any-return]
        except SpotifyOauthError as e:
            log(f"Failed to get access token: {e}", LogLevel.WARNING)
            return None

    def get_cached_token(self) -> dict[str, Any] | None:
        token_info = self.oauth.cache_handler.get_cached_token()
        if not token_info:
            return None
        return self.oauth.validate_token(token_info)  # type: ignore[no-any-return]

    @stamina.retry(on=RETRY_ON, attempts=3)
    def refresh_token(self, refresh_token: str) -> dict[str, Any] | None:
        try:
            return self.oauth.refresh_access_token(refresh_token)  # type: ignore[no-any-return]
        except SpotifyOauthError as e:
            log(f"Failed to refresh token: {e}", LogLevel.WARNING)
            return None
