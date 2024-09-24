import csv
import pandas as pd
import numpy as np

# column index: 0 (Spotify ID), 1 (Artist IDs) , 2 (Track Name) , 3 (Album Name), 4 (Artist Name(s)), 5 (Release Date), 6 (Duration (ms)), 7 (Popularity), 8 (Added By), 9 (Added At), 10 (Genres), 11 (Danceability), 12 (Energy), 13 (Key), 14 (Loudness), 15 (Mode), 16 (Speechiness), 17 (Acousticness), 18 (Instrumentalness), 19 (Liveness), 20 (Valence), 21 (Tempo), 22 (Time Signature)
# BATHROOM CODE: 12344

spotify = pd.read_csv('your_top_songs_2023.csv')
indie = pd.read_csv('indie.csv')
house = pd.read_csv('house_music.csv')

'''
This method calculates the distance between two tables of
values

@param tables_1 First table
@param tables_2 Second table
@return The distance table between each corresponding value
'''
def distance(tables_1, tables_2):
    # if tables_1.size != tables_2.size:
    #     print(tables_1.size, tables_2.size)
    #     raise Exception("Mismatching column sizes")
    radicand = 0
    for i in range(tables_1.size):
        radicand += (tables_2[i] - tables_1[i])**2
    return radicand**(1/2)
    
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
    
    # Retrieves requested attributes
    relevant_table = data_table.loc[:, ['Track Name', 'Artist Name(s)'] + attributes]
    # Finds how close they are to maximized song parameters
    att_arr = np.array([relevant_table[i] for i in attributes])
    distance_column = distance(np.ones(len(attributes)), att_arr)
    table_with_distances = relevant_table.assign(distances = distance_column)
    # Finds the kth maximum songs based on song parameters
    sorted_table = table_with_distances.sort_values('distances').head(k)
    songs_and_artists = sorted_table.loc[:, ['Track Name', 'Artist Name(s)']]

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

top_songs = songs_by_attributes(indie, ["Tempo"], 10)
make_playlist_csv(top_songs)
