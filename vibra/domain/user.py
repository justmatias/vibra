from typing import Any, Self

from pydantic import BaseModel


class SpotifyUser(BaseModel):
    id: str
    display_name: str
    email: str | None
    country: str | None
    product: str | None
    image_url: str | None
    followers: int

    @classmethod
    def from_api_response(cls, data: dict[str, Any]) -> Self:
        """Create SpotifyUser from Spotify API response."""
        images = data.get("images", [])
        image_url = images[0]["url"] if images else None

        return cls(
            id=data["id"],
            display_name=data.get("display_name", data["id"]),
            email=data.get("email"),
            country=data.get("country"),
            product=data.get("product"),
            image_url=image_url,
            followers=data.get("followers", {}).get("total", 0),
        )
