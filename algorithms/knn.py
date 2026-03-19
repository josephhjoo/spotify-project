# The recommendation algorithm (brain)

import numpy as np

def recommend_songs(data_table, attributes, k):

    # Avoids modification of original data
    data_table = data_table.copy()

    distance = 0

    # Calculate how far each song is from the "ideal" attribute value
    for att in attributes:
        distance += (1 - data_table[att]) ** 2

    # Normalizes distance score based on number of attributes
    data_table["distance"] = np.sqrt(distance / len(attributes))

    # Selects the k top songs of the sorted list
    sorted_table = data_table.sort_values("distance").head(k)

    columns_to_return = [
        "Track Name",
        "Artist Name(s)",
        "Spotify ID",
    ] + attributes

    return sorted_table.loc[:, columns_to_return]