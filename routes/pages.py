# Handles routing to all pages of the app

import csv
import spotipy
from flask import Blueprint, redirect, render_template, request
from services.playlist_services import make_playlist_csv, playlist_attribute_summary
from algorithms.knn import recommend_songs
from auth.spotify_client import get_spotify_oauth
from data.loader import genre_df
from media.spotify_media import get_album_covers

# Blueprint for user-facing pages of the app (frontend)
pages_bp = Blueprint("pages", __name__)

# List of audio features the user can choose from
ATTRIBUTES = [
    "Popularity",
    "Danceability",
    "Energy",
    "Loudness",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo",
]

# Makes sure the user is connected to Spotify before using the app
def _require_spotify_login():
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.cache_handler.get_cached_token()

    if not sp_oauth.validate_token(token_info):
        return redirect(sp_oauth.get_authorize_url())

    return None

# Runs the algorithm, generates the playlist
def _generate_playlist(genre: str, selected_attributes: list[str], playlist_length: int):
    data_table = genre_df(genre)
    sp = spotipy.Spotify(auth_manager=get_spotify_oauth())

    playlist = recommend_songs(data_table, selected_attributes, playlist_length)
    playlist["Album Cover"] = get_album_covers(playlist["Spotify ID"], sp)

    return playlist

# Homepage route (genre selection)
@pages_bp.get("/index.html")
def index():
    auth_redirect = _require_spotify_login()
    if auth_redirect:
        return auth_redirect
    return render_template("index.html")

# Page for attribute selection
@pages_bp.route("/attributes/<genre>", methods=["GET", "POST"])
def attributes_page(genre):
    auth_redirect = _require_spotify_login()
    if auth_redirect:
        return auth_redirect

    genre_display_names = {
        "indie": "Indie",
        "house": "House",
        "rap": "Rap",
        "rb": "R&B",
    }

    if genre not in genre_display_names:
        return "Genre not found", 404

    if request.method == "POST":
        selected_attributes = request.form.getlist("attributes")[0].split(",")
        playlist_length = int(request.form["playlist_length"])

        playlist = _generate_playlist(
            genre,
            selected_attributes,
            playlist_length
        )

        summary = playlist_attribute_summary(playlist, selected_attributes)
        playlist_csv = make_playlist_csv(playlist)

        return render_template(
            "playlist.html",
            playlist=playlist.to_dict(orient="records"),
            playlist_csv=playlist_csv,
            summary=summary
        )

    return render_template(
        "attributes.html",
        attributes=ATTRIBUTES,
        genre=genre,
        genre_display=genre_display_names[genre]
    )

# Page to import playlist into user's Spotify library
@pages_bp.post("/import_to_spotify")
def import_to_spotify():
    sp_oauth = get_spotify_oauth()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return redirect(sp_oauth.get_authorize_url())

    sp = spotipy.Spotify(auth=token_info["access_token"])

    playlist_csv = request.form["playlist_csv"]
    track_uris: list[str] = []

    with open(playlist_csv, "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            spotify_id = row[2] if len(row) > 2 else ""
            if spotify_id:
                track_uris.append(spotify_id)

    if not track_uris:
        return "No tracks found to add to the playlist.", 400

    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, "Generated Playlist", public=True)
    sp.user_playlist_add_tracks(user_id, playlist["id"], track_uris)

    return render_template("success.html")