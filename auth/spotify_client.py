# Manages communication with the Spotify API

import os
import spotipy
from flask import session
from spotipy import Spotify
from spotipy.cache_handler import FlaskSessionCacheHandler
from spotipy.oauth2 import SpotifyOAuth


# Helper function, loads environment variables (Spotify keys)
def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(
        f"Missing required environment variable {name}. "
        "Create a .env file or export it in your shell before running."
    )

# Creates Spotify object used for authentication
# Handles login, manages user's access token
def get_spotify_oauth() -> SpotifyOAuth:
    cache_handler = FlaskSessionCacheHandler(session)

    client_id = _required_env("SPOTIPY_CLIENT_ID")
    client_secret = _required_env("SPOTIPY_CLIENT_SECRET")
    redirect_uri = _required_env("SPOTIPY_REDIRECT_URI")
    scope = os.getenv(
        "SPOTIPY_SCOPE",
        "playlist-modify-public playlist-modify-private"
    )

    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_handler=cache_handler,
        show_dialog=True,
    )

# Creates Spotify API client using the access token
# Allows interactions with Spotify (importing playlists to user's library)
def get_spotify_client() -> Spotify:
    token_info = get_spotify_oauth().get_cached_token()
    return spotipy.Spotify(auth=token_info["access_token"])