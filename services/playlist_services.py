# Handles logic for creating and preparing playlists

import csv
from pathlib import Path
from data.loader import genre_df
from algorithms.knn import recommend_songs
from media.spotify_media import get_album_covers

# Generates playlist
def generate_playlist(genre, attributes, k, sp):
    data_table = genre_df(genre)

    playlist = recommend_songs(
        data_table,
        attributes,
        k
    )

    playlist["Album Cover"] = get_album_covers(
        playlist["Spotify ID"],
        sp
    )

    return playlist

# Saves generated playlist as a csv file
def make_playlist_csv(df):
    project_root = Path(__file__).resolve().parents[1]
    static_dir = project_root / "static"
    static_dir.mkdir(exist_ok=True)

    file_path = static_dir / "playlist.csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["TITLE", "ARTIST", "SPOTIFY_ID"])

        for _, row in df.iterrows():
            writer.writerow([
                row["Track Name"],
                row["Artist Name(s)"],
                row["Spotify ID"],
            ])

    return str(file_path)

# Calculates average value of each selected attribute (for stats display)
def playlist_attribute_summary(df, attributes):
    summary = {}

    for attr in attributes:
        if attr in df.columns:
            summary[attr] = round(df[attr].mean(), 2)

    return summary