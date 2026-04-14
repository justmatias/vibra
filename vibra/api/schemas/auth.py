from typing import Any, Self

from pydantic import BaseModel


class AuthorizeResponse(BaseModel):
    auth_url: str


class CallbackRequest(BaseModel):
    code: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int
    expires_at: int | None = None
    scope: str | None = None

    @classmethod
    def from_spotipy(cls, token: dict[str, Any]) -> Self:
        return cls(
            access_token=token["access_token"],
            refresh_token=token.get("refresh_token"),
            expires_in=token.get("expires_in", 3600),
            expires_at=token.get("expires_at"),
            scope=token.get("scope"),
        )


class LogoutResponse(BaseModel):
    cleared: bool
