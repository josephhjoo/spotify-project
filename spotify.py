import csv
import pandas as pd
import numpy as np

# column index: 0 (Spotify ID), 1 (Artist IDs) , 2 (Track Name) , 3 (Album Name), 4 (Artist Name(s)), 5 (Release Date), 6 (Duration (ms)), 7 (Popularity), 8 (Added By), 9 (Added At), 10 (Genres), 11 (Danceability), 12 (Energy), 13 (Key), 14 (Loudness), 15 (Mode), 16 (Speechiness), 17 (Acousticness), 18 (Instrumentalness), 19 (Liveness), 20 (Valence), 21 (Tempo), 22 (Time Signature)
# BATHROOM CODE: 12344

spotify = pd.read_csv('your_top_songs_2023.csv')
indie = pd.read_csv('indie.csv')
house = pd.read_csv('house_music.csv')
    
'''
This method returns a Dataframe of k songs which matches a 
list of attributes

@param data_table Genre of music to pull from
@param attributes A list of attributes the sort from
@param k          Number of songs returned
@return A Dataframe corresponding the attributes sorted by
'''
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
    songs_and_artists = sorted_table.loc[:, ['Track Name', 'Artist Name(s)']].head(k)

    return songs_and_artists

'''
This method generates a CSV file containing the trackname and artist
of a provided Dataframe

@param df Dataframe to retrieve from
'''
def make_playlist_csv(df):
    playlist_list = df.values.tolist()
    with open('playlist', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["TITLE","ARTIST"]) 
        writer.writerows(playlist_list)

top_songs = songs_by_attributes(indie, ["Speechiness", "Liveness", "Acousticness"], 10)
make_playlist_csv(top_songs)
