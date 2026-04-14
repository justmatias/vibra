import pytest

from vibra.infrastructure.genius.client import GeniusClient


@pytest.mark.vcr
def test_search_song(
    genius_client: GeniusClient,
    song_search_query: tuple[str, str],
) -> None:
    title, artist = song_search_query
    lyrics = genius_client.search_song(title, artist)
    assert isinstance(lyrics, str)
    # If the song is found, lyrics should not be empty.
    # However, if credentials are bad or song not found, it might be empty.
    # We expect these valid songs to be found.
    assert len(lyrics) > 0
