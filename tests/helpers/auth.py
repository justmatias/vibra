from spotipy.oauth2 import SpotifyOauthError

from vibra.infrastructure.auth import SpotifyAuthManager


def get_spotify_token() -> str | None:
    """
    Get a valid Spotify access token from the cache.
    Returns None if no valid token is found in the cache.
    """
    try:
        auth_manager = SpotifyAuthManager()
        token_info = auth_manager.get_cached_token()

        if not token_info or not token_info.get("access_token"):
            return None
        token_info = auth_manager.oauth.validate_token(token_info)
        return token_info.get("access_token")  # type: ignore[no-any-return]
    except SpotifyOauthError:
        return None
