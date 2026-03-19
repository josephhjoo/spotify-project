# Handles Spotify Authentication (for playlist import purposes)

from flask import Blueprint, redirect, request, url_for, session
from auth.spotify_client import get_spotify_oauth


# Blueprint that handles Spotify authentication routes
spotify_auth_bp = Blueprint("spotify_auth", __name__)

# Checks if user has already logged in
@spotify_auth_bp.get("/")
def home():
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.cache_handler.get_cached_token()

    # If not, redirect to login
    if not sp_oauth.validate_token(token_info):
        session.clear()
        return redirect(sp_oauth.get_authorize_url())

    # If so, direct to app home page
    return redirect(url_for("pages.index"))

# Redirects after the user logs in
@spotify_auth_bp.get("/callback")
def callback():
    sp_oauth = get_spotify_oauth()

    # Exchange the authorization code from Spotify for an access token
    sp_oauth.get_access_token(request.args["code"])
    return redirect(url_for("pages.index"))

# Logout route: clears the user's session
@spotify_auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("spotify_auth.home"))