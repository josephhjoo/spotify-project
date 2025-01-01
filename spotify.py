import csv, os
import pandas as pd
import numpy as np
import flask as flask
from flask import Flask, request

# column index: 0 (Spotify ID), 1 (Artist IDs) , 2 (Track Name) , 3 (Album Name), 4 (Artist Name(s)), 5 (Release Date), 6 (Duration (ms)), 7 (Popularity), 8 (Added By), 9 (Added At), 10 (Genres), 11 (Danceability), 12 (Energy), 13 (Key), 14 (Loudness), 15 (Mode), 16 (Speechiness), 17 (Acousticness), 18 (Instrumentalness), 19 (Liveness), 20 (Valence), 21 (Tempo), 22 (Time Signature)
# BATHROOM CODE: 12344
        
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


def distance_infinite_d(data_table, attributes: list):
    to_be_square_rooted = 0
    for att in attributes:
        to_be_square_rooted += (1 - data_table[att])**2
    return np.sqrt(to_be_square_rooted)


"""
This method returns a Dataframe of k songs which matches a 
list of attributes

@param data_table Genre of music to pull from
@param attributes A list of attributes the sort from
@param k          Number of songs returned
@return A Dataframe corresponding the attributes sorted by
"""

def songs_by_attributes(data_table, attributes: list, k: int, output_file="playlist.csv"):
    if 0 > k > data_table.shape[0]:
        print("Invalid number of songs")
        return None

    for i in attributes:
        if i not in data_table.columns:
            print(f"{i} is not a valid song parameter")
            return None

    distance_column = distance_infinite_d(data_table, attributes)
    data_table["distances"] = distance_column
    sorted_table = data_table.sort_values('distances', ascending=False).head(k)
    
    # Add the Spotify track ID (assuming it's in the 'Spotify ID' column)
    playlist = sorted_table.loc[:, ['Track Name', 'Artist Name(s)', 'Spotify ID']]  # Add 'Spotify ID'

    # Save the playlist to a CSV file in the project folder
    project_folder = os.getcwd()  # Get the current working directory
    output_path = os.path.join(project_folder, output_file)

    try:
        playlist.to_csv(output_path, index=False)
        print(f"Playlist saved to {output_path}")
    except Exception as e:
        print(f"Failed to save playlist: {e}")
    
    return playlist



"""
This method generates a CSV file containing the trackname and artist
of a provided Dataframe

@param df Dataframe to retrieve from
"""
def make_playlist_csv(df):
    playlist_list = df.values.tolist()
    file_path = os.path.join(os.getcwd(), "static", "playlist.csv")  # Save to the "static" folder
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["TITLE", "ARTIST"])
        writer.writerows(playlist_list)
    return file_path

# indie = genre_df("house_music")
# top_songs = songs_by_attributes(indie, ["Liveness", "Acousticness", "Tempo"], 10)
# make_playlist_csv(top_songs)

indie = genre_df("house")
top_songs = songs_by_attributes(indie, ["Popularity"], 1)
make_playlist_csv(top_songs)
