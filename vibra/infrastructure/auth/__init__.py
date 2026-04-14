"""Auth manager implementations.

Contains the production SpotifyAuthManager and a FakeAuthManager for testing.
Both satisfy the ``AuthManager`` protocol defined in ``vibra.domain``.
"""

from .fake import FakeAuthManager
from .spotify import SpotifyAuthManager

__all__ = ["FakeAuthManager", "SpotifyAuthManager"]
