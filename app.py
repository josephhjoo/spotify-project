from dotenv import load_dotenv

# Loads .env file for Spotify API keys
load_dotenv()

from flask import Flask
from routes.pages import pages_bp
from auth.spotify_auth import spotify_auth_bp

 # Create the web app and securely manage session data
app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

# Registers main page and OAuth authentication routes
app.register_blueprint(pages_bp)
app.register_blueprint(spotify_auth_bp)

# Starts the local web server
if __name__ == "__main__":
    app.run(debug=True)