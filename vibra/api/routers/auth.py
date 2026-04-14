from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from vibra.api.dependencies import (
    get_auth_manager,
    get_bearer_token,
    get_spotify_client_for_token,
)
from vibra.api.schemas import (
    AuthorizeResponse,
    CallbackRequest,
    LogoutResponse,
    RefreshRequest,
    TokenResponse,
)
from vibra.domain import SpotifyUser
from vibra.infrastructure.spotify.auth_manager import SpotifyAuthManager
from vibra.utils import Settings

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/authorize")
def authorize(
    auth: Annotated[SpotifyAuthManager, Depends(get_auth_manager)],
) -> AuthorizeResponse:
    url = auth.get_auth_url()
    return AuthorizeResponse(auth_url=url)


@router.post("/callback")
def callback(
    body: CallbackRequest,
    auth: Annotated[SpotifyAuthManager, Depends(get_auth_manager)],
) -> TokenResponse:
    token = auth.get_access_token(body.code)
    if not token:
        raise HTTPException(
            status_code=401, detail="Failed to exchange authorization code"
        )
    return TokenResponse.from_spotipy(token)


@router.post("/refresh")
def refresh(
    body: RefreshRequest,
    auth: Annotated[SpotifyAuthManager, Depends(get_auth_manager)],
) -> TokenResponse:
    token = auth.refresh_token(body.refresh_token)
    if not token:
        raise HTTPException(status_code=401, detail="Failed to refresh token")

    return TokenResponse.from_spotipy(token)


@router.post("/logout")
def logout() -> LogoutResponse:
    cache_file = Settings.CACHE_PATH / ".spotify_cache"
    cleared = cache_file.exists()
    if cleared:
        cache_file.unlink()

    return LogoutResponse(cleared=cleared)


@router.get("/me")
def me(
    token: Annotated[str | None, Depends(get_bearer_token)],
) -> SpotifyUser:
    if not token:
        raise HTTPException(status_code=401, detail="Invalid access token")
    client = get_spotify_client_for_token(token)
    return client.current_user
