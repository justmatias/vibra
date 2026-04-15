from unittest.mock import patch

import pytest

from vibra.infrastructure.lyrics.client import GeniusClient


def test_search_song_returns_empty_string_on_exception(
    genius_client: GeniusClient,
) -> None:
    with patch.object(genius_client, "_fetch_lyrics", side_effect=Exception("timeout")):
        result = genius_client.search_song("Some Song", "Some Artist")

    assert result == ""


@pytest.mark.vcr
def test_search_song(
    genius_client: GeniusClient,
    song_search_query: tuple[str, str],
) -> None:
    title, artist = song_search_query
    lyrics = genius_client.search_song(title, artist)
    assert isinstance(lyrics, str)
    assert len(lyrics) > 0
