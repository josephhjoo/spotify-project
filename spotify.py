import csv, os
import pandas as pd
import numpy as np
import flask as flask
from flask import Flask, request

# column index: 0 (Spotify ID), 1 (Artist IDs) , 2 (Track Name) , 3 (Album Name), 4 (Artist Name(s)), 5 (Release Date), 6 (Duration (ms)), 7 (Popularity), 8 (Added By), 9 (Added At), 10 (Genres), 11 (Danceability), 12 (Energy), 13 (Key), 14 (Loudness), 15 (Mode), 16 (Speechiness), 17 (Acousticness), 18 (Instrumentalness), 19 (Liveness), 20 (Valence), 21 (Tempo), 22 (Time Signature)
# BATHROOM CODE: 12344

app = Flask(__name__)
@app.route("/")
def home(name=None):
    return flask.render_template('home.html', name=name)

@app.route("/genres")
def genre_selection(name=None):
    return flask.render_template('genres.html', name=name)

@app.route("/attributes")
def attribute_selection(name=None):
    return flask.render_template('attributes.html', name=name)

# Testing html
@app.route("/indie")
def indie_test(name=None):
    return flask.render_template('indie.html', name=name)

# if __name__ == "__main__":
#     app.run(debug=True)
    
@app.route('/results', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'POST':
        genre = request.form.get("genre_selection")
        df = genre_df(genre)
        
"""
This method selects which CSV file to generate a playlist 
from
@param A string representing the genre desired
@return A Dataframe containing the respective spotify information
"""
def genre_df(genre):
    csv_name = genre + ".csv"
    for root, dirs, files in os.walk("."):
        if csv_name in files:
            return pd.read_csv(csv_name)
    raise Exception("No such genre exists")

"""
This method returns a Dataframe of k songs which matches a 
list of attributes

@param data_table Genre of music to pull from
@param attributes A list of attributes the sort from
@param k          Number of songs returned
@return A Dataframe corresponding the attributes sorted by
"""
def songs_by_attributes(data_table, attributes, k):
    # returns table with k rows that relate most to three attributes of choice (v1, v2, v3) from data_table
    # Checks if k is a valid number of songs
    if 0 > k > data_table.shape[0]:
        print("Invalid number of songs")
        return None

    # Checks if parameters are valid song parameters
    for i in attributes:
        if i not in data_table.columns:
            print(f"{i} is not a valid song parameter")
            return None

    # Sorts by requested attributes
    sorted_table = data_table.sort_values(by=attributes, ascending=False)

    # Finds the kth maximum songs based on song parameters
    songs_and_artists = sorted_table.loc[:, ["Track Name", "Artist Name(s)"]].head(k)

    return songs_and_artists


"""
This method generates a CSV file containing the trackname and artist
of a provided Dataframe

@param df Dataframe to retrieve from
"""
def make_playlist_csv(df):
    playlist_list = df.values.tolist()
    with open("playlist", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["TITLE", "ARTIST"])
        writer.writerows(playlist_list)

indie = genre_df("rap")
top_songs = songs_by_attributes(indie, ["Speechiness", "Liveness", "Acousticness"], 5)
make_playlist_csv(top_songs)
