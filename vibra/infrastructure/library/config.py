from spotipy.exceptions import SpotifyException

RETRY_ON = (SpotifyException, ConnectionError, TimeoutError)
