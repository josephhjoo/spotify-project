import os, csv

from flask import Flask, render_template, request, redirect, url_for, session
from spotify import genre_df, songs_by_attributes, make_playlist_csv
import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

cache_handler = FlaskSessionCacheHandler(session)

# Spotify app credentials
SPOTIPY_CLIENT_ID = "984f8ba6318442d68c90f96564de853a"
SPOTIPY_CLIENT_SECRET = "de9359d67c684c0ebf8b0720b6d3ee6e"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Spotify scope for playlist management
SCOPE = "playlist-modify-public playlist-modify-private"

cache_handler = FlaskSessionCacheHandler(session)

# Create SpotifyOAuth object
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope=SCOPE,
                        cache_handler=cache_handler,
                        show_dialog=True)

sp = Spotify(auth_manager=sp_oauth)

# Define the available attributes
ATTRIBUTES = ["Popularity", "Danceability", "Energy", "Loudness", "Speechiness", 
              "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo"]

##### SPOTIFY MISC #####

@app.route("/")
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for("index"))

@app.route("/callback")
def callback():
    sp_oauth.get_access_token(request.args["code"])
    return redirect(url_for("index"))


##### DISPLAY PAGES #####

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route("/playlist")
def playlist():
    try:
        playlist_url = make_playlist_csv(playlist)  # Assuming `playlist` is the dataframe you generated
        return render_template("playlist.html", playlist=playlist.values.tolist(), playlist_url=playlist_url)
    except Exception as e:
        return str(e), 400

##### GENRE PAGES #####

@app.route("/attributes_indie.html", methods=["GET", "POST"])
def attributes_indie():
    if request.method == "POST":
        selected_attributes = request.form.getlist("attributes")
        playlist_length = int(request.form["playlist_length"])

        try:
            data_table = genre_df("indie")
            playlist = songs_by_attributes(data_table, selected_attributes, playlist_length)
            return render_template("playlist.html", playlist=playlist.values.tolist())
        except Exception as e:
            return str(e), 400

    return render_template("attributes_indie.html", attributes=ATTRIBUTES)

@app.route("/attributes_house.html", methods=["GET", "POST"])
def attributes_house():
    if request.method == "POST":
        selected_attributes = request.form.getlist("attributes")
        playlist_length = int(request.form["playlist_length"])

        try:
            data_table = genre_df("house")
            playlist = songs_by_attributes(data_table, selected_attributes, playlist_length)
            return render_template("playlist.html", playlist=playlist.values.tolist())
        except Exception as e:
            return str(e), 400

    return render_template("attributes_house.html", attributes=ATTRIBUTES)

@app.route("/attributes_rap.html", methods=["GET", "POST"])
def attributes_rap():
    if request.method == "POST":
        selected_attributes = request.form.getlist("attributes")
        playlist_length = int(request.form["playlist_length"])

        try:
            data_table = genre_df("rap")
            playlist = songs_by_attributes(data_table, selected_attributes, playlist_length)
            return render_template("playlist.html", playlist=playlist.values.tolist())
        except Exception as e:
            return str(e), 400

    return render_template("attributes_rap.html", attributes=ATTRIBUTES)

@app.route("/attributes_rb.html", methods=["GET", "POST"])
def attributes_rb():
    if request.method == "POST":
        selected_attributes = request.form.getlist("attributes")
        playlist_length = int(request.form["playlist_length"])

        try:
            data_table = genre_df("rb")
            playlist = songs_by_attributes(data_table, selected_attributes, playlist_length)
            return render_template("playlist.html", playlist=playlist.values.tolist())
        except Exception as e:
            return str(e), 400

    return render_template("attributes_rb.html", attributes=ATTRIBUTES)


##### IMPORT FUNCTION #####

@app.route("/import_to_spotify", methods=["POST"])
def import_to_spotify():
    try:
        # Step 1: Get the user's Spotify access token
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            # Redirect to Spotify OAuth if we don't have a cached token
            return redirect(sp_oauth.get_authorize_url())

        sp = spotipy.Spotify(auth=token_info['access_token'])

        # Step 2: Read the CSV file containing the playlist (adjust path as needed)
        playlist_csv = "playlist.csv"  # Replace with the actual path to your generated playlist
        track_uris = []

        with open(playlist_csv, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                spotify_id = row[2]  # Assuming the 'Spotify ID' is the third column in the CSV
                if spotify_id:  # Ensure the Spotify ID is not empty
                    track_uris.append(spotify_id)

        if not track_uris:
            return "No tracks found to add to the playlist.", 400

        # Step 4: Create a new playlist in the user's Spotify account
        user_id = sp.current_user()['id']
        playlist = sp.user_playlist_create(user_id, "Generated Playlist", public=True)

        # Step 5: Add tracks to the playlist
        sp.user_playlist_add_tracks(user_id, playlist['id'], track_uris)

        # Render the success page
        return render_template("success.html")

    except Exception as e:
        return f"Error: {e}", 400




if __name__ == "__main__":
    app.run(debug=True)
