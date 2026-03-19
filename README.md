# Spotify Project (Flask)

## Setup

### 1) Create your Spotify app

- Go to the Spotify Developer Dashboard and create an app.
- Add this Redirect URI in the app settings:
  - `http://127.0.0.1:5000/callback`

### 2) Configure environment variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

Required:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`

Optional:

- `FLASK_SECRET_KEY` (recommended)
- `SPOTIPY_SCOPE` (defaults to `playlist-modify-public playlist-modify-private`)

Then export the variables into your shell (pick one approach):

```bash
set -a
source .env
set +a
```

## Run the web app

```bash
python app.py
```

Then open `http://127.0.0.1:5000/index.html`.

## Token script (optional)

`run.sh` requests a client-credentials token and now reads:

- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`

Example:

```bash
set -a
source .env
set +a

bash run.sh
```

