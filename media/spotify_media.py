# Shows playlist album covers on playlist output page

def get_album_covers(spotify_ids, sp):

    covers = []

    for spotify_id in spotify_ids:

        try:
            # Finds album for every track (spotify_id)
            track = sp.track(spotify_id)
            covers.append(track["album"]["images"][0]["url"])

        except Exception:
            covers.append("")

    return covers