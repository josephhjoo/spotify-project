# Loads the data used by the recommendation system

from pathlib import Path
import pandas as pd
from data.preprocessing import normalize_columns

# Folder where all the data is stored
DATA_DIR = Path(__file__).resolve().parent / "stats_csvs"

# Audio features
NORMALIZED_COLUMNS = [
    "Popularity",
    "Danceability",
    "Energy",
    "Loudness",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo"
]

# Loads the dataset for a given genre
def genre_df(genre):

    path = DATA_DIR / f"{genre}.csv"

    # Ensures the dataset exists
    if not path.exists():
        raise FileNotFoundError(f"No dataset for {genre}")

    # Loads the csv into a dataframe
    df = pd.read_csv(path)

    # Normalizes the audio feature columns so they are on the same scale
    df = normalize_columns(df, NORMALIZED_COLUMNS)

    return df