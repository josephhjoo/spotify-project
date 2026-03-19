# Functions for prepping datasets

import pandas as pd

# Normalizes all numerical columns so the values fall between 0 and 1
def normalize_columns(df, columns):

    # Work on a copy
    df = df.copy()

    for col in columns:
        if col in df.columns:
            min_val = df[col].min()
            max_val = df[col].max()

            # Apply min-max normalization (standard normalization)
            # (value - min) / (max - min)
            if max_val != min_val:
                df[col] = (df[col] - min_val) / (max_val - min_val)

    return df