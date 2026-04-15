import pytest

from vibra.infrastructure import GeniusClient


@pytest.fixture
def genius_client() -> GeniusClient:
    return GeniusClient()


@pytest.fixture(
    params=[
        ("Blinding Lights", "The Weeknd"),
        ("Rich Flex - Live", "Drake & 21 Savage"),
    ],
    ids=["no_sanitized", "sanitized"],
)
def song_search_query(request: pytest.FixtureRequest) -> tuple[str, str]:
    return request.param  # type: ignore[no-any-return]
