from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain.user import SpotifyUser


def test_spotify_user_from_api_response(
    spotify_user_factory: ModelFactory[SpotifyUser],
) -> None:
    user_data = spotify_user_factory.build().model_dump(by_alias=True)
    # Patch followers to match API response structure (dict) instead of domain model (int)
    # The domain model expects 'followers' as int, but the API returns it as dict.
    # We simulate the API/raw data structure here.
    user_data["followers"] = {"total": 100}
    user_data["images"] = [
        {"url": "http://example.com/pic.jpg", "height": 100, "width": 100}
    ]

    user = SpotifyUser.from_api_response(user_data)

    assert user.id == user_data["id"]
    assert user.display_name == user_data["display_name"]
    assert user.email == user_data["email"]
    assert user.image_url == "http://example.com/pic.jpg"
    assert user.followers == 100
