"""Polyfactory fixtures for test data generation.

This module contains all polyfactory factory fixtures used across the test suite.
It is registered as a pytest plugin in conftest.py.
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture

from vibra.domain import (
    EnrichedTrack,
    SavedTrack,
    SpotifyAlbum,
    SpotifyArtist,
    SpotifyImage,
    SpotifyTrack,
    SpotifyUser,
    SyncProgress,
)


# Domain: Track factories
@register_fixture(name="spotify_image_factory")
class SpotifyImageFactory(ModelFactory[SpotifyImage]): ...


@register_fixture(name="spotify_artist_factory")
class SpotifyArtistFactory(ModelFactory[SpotifyArtist]): ...


@register_fixture(name="spotify_album_factory")
class SpotifyAlbumFactory(ModelFactory[SpotifyAlbum]): ...


@register_fixture(name="spotify_track_factory")
class SpotifyTrackFactory(ModelFactory[SpotifyTrack]):
    __random_seed__ = 123


@register_fixture(name="saved_track_factory")
class SavedTrackFactory(ModelFactory[SavedTrack]): ...


# Domain: User factories
@register_fixture(name="spotify_user_factory")
class SpotifyUserFactory(ModelFactory[SpotifyUser]):
    __random_seed__ = 123


# Services: Domain model factories
@register_fixture(name="sync_progress_factory")
class SyncProgressFactory(ModelFactory[SyncProgress]): ...


@register_fixture(name="enriched_track_factory")
class EnrichedTrackFactory(ModelFactory[EnrichedTrack]): ...
