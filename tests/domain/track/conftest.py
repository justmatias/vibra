import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from vibra.domain.track import (
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyImage,
    SpotifyTrack,
)


@pytest.fixture
def album_with_image(
    spotify_image_factory: ModelFactory[SpotifyImage],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
) -> SpotifyAlbum:
    image = spotify_image_factory.build(url="http://example.com/image.jpg")
    return spotify_album_factory.build(images=[image])


@pytest.fixture
def track_with_artists(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_album_factory: ModelFactory[SpotifyAlbum],
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    artist1 = spotify_artist_factory.build(name="Artist One")
    artist2 = spotify_artist_factory.build(name="Artist Two")
    album = spotify_album_factory.build()

    return spotify_track_factory.build(
        artists=[artist1, artist2],
        album=album,
        external_urls={"spotify": "http://spotify.com/track/123"},
    )


@pytest.fixture
def track_without_spotify_url(
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    return spotify_track_factory.build(external_urls={})


@pytest.fixture
def artist_with_multiple_genres(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
) -> SpotifyArtist:
    return spotify_artist_factory.build(genres=["rock", "pop", "indie"])


@pytest.fixture
def artist_with_single_genre(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
) -> SpotifyArtist:
    return spotify_artist_factory.build(genres=["jazz"])


@pytest.fixture
def artist_with_no_genres(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
) -> SpotifyArtist:
    return spotify_artist_factory.build(genres=[])


@pytest.fixture
def track_with_multiple_artist_genres(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    artist1 = spotify_artist_factory.build(genres=["rock", "pop"])
    artist2 = spotify_artist_factory.build(genres=["indie", "alternative"])
    return spotify_track_factory.build(artists=[artist1, artist2])


@pytest.fixture
def track_with_duplicate_genres(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    return spotify_track_factory.build(
        artists=[
            spotify_artist_factory.build(genres=["rock", "pop", "indie"]),
            spotify_artist_factory.build(genres=["indie", "rock", "alternative"]),
        ]
    )


@pytest.fixture
def track_with_no_genres(
    spotify_artist_factory: ModelFactory[SpotifyArtist],
    spotify_track_factory: ModelFactory[SpotifyTrack],
) -> SpotifyTrack:
    artist = spotify_artist_factory.build(genres=[])
    return spotify_track_factory.build(artists=[artist])
