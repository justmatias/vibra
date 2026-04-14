import pytest

from vibra.domain import SavedTrack, SpotifyArtist, SpotifyUser
from vibra.infrastructure.spotify import SpotifyClient


@pytest.mark.vcr
def test_get_current_user(spotify_client: SpotifyClient) -> None:
    user = spotify_client.current_user
    assert isinstance(user, SpotifyUser)


@pytest.mark.vcr
def test_get_liked_songs(spotify_client: SpotifyClient) -> None:
    response = spotify_client.get_liked_songs(limit=5)
    assert response.get("items")
    assert len(response["items"]) <= 5


@pytest.mark.vcr
def test_get_all_liked_songs(spotify_client: SpotifyClient) -> None:
    tracks = spotify_client.get_all_liked_songs(max_tracks=10)
    assert isinstance(tracks, list)
    assert all(isinstance(track, SavedTrack) for track in tracks)
    assert len(tracks) <= 10


@pytest.mark.vcr
def test_get_artists(spotify_client: SpotifyClient, artist_ids: list[str]) -> None:
    artists = spotify_client.get_artists(artist_ids)
    assert len(artists) == len(artist_ids)
    assert all(isinstance(artist, SpotifyArtist) for artist in artists)
