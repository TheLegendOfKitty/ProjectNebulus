import os
from flask import Flask, session, request, redirect
from flask_session import Session
import spotipy
import uuid
from SwSpotify import spotify


# In order to get Spotipy to work, you must install the latest version with cloning the repo with the following command:
# pip3 install git+https://github.com/plamere/spotipy
SPOTIPY_CLIENT_ID = "846095b9ce934b0da3e0aaf3adbf600c"
SPOTIPY_CLIENT_SECRET = "1d79c77cee124d8f8e20b16f720d65e8"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:9080/"


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(64)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./.flask_session/"
Session(app)

caches_folder = "./.spotify_caches/"
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path():
    return caches_folder + session.get("uuid")


@app.route("/")
def index():
    if not session.get("uuid"):
        # Step 1. Visitor is unknown, give random ID
        session["uuid"] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect("/")

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return f'<h2><a href="{auth_url}">Sign in</a></h2>'

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return (
        f'<h2>Hi {spotify.me()["display_name"]}, '
        f'<small><a href="/sign_out">[sign out]<a/></small></h2>'
        f'<a href="/playlists">my playlists</a> | '
        f'<a href="/currently_playing">currently playing</a> | '
        f'<a href="/current_user">me</a>'
    )


@app.route("/sign_out")
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect("/")


@app.route("/playlists")
def playlists():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@app.route("/currently_playing")
def currently_playing():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    track = spotify.current_user_playing_track()
    if not track is None:
        return track
    return "No track currently playing."


@app.route("/current_user")
def current_user():
    cache_handler = spotipy.cache_handler.CacheFileHandler(
        cache_path=session_cache_path()
    )
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        scope="user-read-currently-playing playlist-modify-private",
        cache_handler=cache_handler,
        show_dialog=True,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect("/")
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


"""
Following lines allow application to be run more conveniently with
`python app.py` (Make sure you're using python3)
(Also includes directive to leverage pythons threading capacity.)
"""
if __name__ == "__main__":
    app.run(threaded=True, port=int(os.environ.get("PORT", 9080)))