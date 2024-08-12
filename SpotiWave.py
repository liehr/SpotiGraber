import os
import time

import requests
import spotipy
from spotipy import SpotifyOAuth
from termcolor import cprint

# Constants for Spotify API credentials and redirect URI
SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID'  # Must be added to the Spotify app settings
SPOTIPY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'  # Must be added to the Spotify app settings
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'  # Must be added to the Spotify app settings
SCOPE = "user-read-currently-playing, user-read-playback-state, user-modify-playback-state"
TOKEN_REFRESH_INTERVAL = 2800  # Time in seconds

# Base URL for constructing the scannable image link
BASE_IMAGE_URL = 'https://scannables.scdn.co/uri/plain/png/000000/white/640/spotify:track:'
SAVE_PATH = os.path.expanduser("~/Desktop/spotify_code.png")

# Initialize the Spotify OAuth object
oauth_object = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                            client_secret=SPOTIPY_CLIENT_SECRET,
                            redirect_uri=SPOTIPY_REDIRECT_URI,
                            scope=SCOPE)


def get_spotify_object():
    """Authenticate and return a Spotify object."""
    try:
        access_token = oauth_object.get_access_token(as_dict=False, check_cache=False)
        return spotipy.Spotify(auth=access_token)
    except Exception as e:
        cprint(f"Failed to authenticate with Spotify: {e}", "red", attrs=["bold"])
        return None


def download_image(url, save_path):
    """Download an image from the specified URL and save it to the given path."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        cprint(f"Image saved to {save_path}", "green")
    except requests.RequestException as e:
        cprint(f"Failed to download image: {e}", "red", attrs=["bold"])


def extract_track_id(spotify_url):
    """Extract the track ID from the Spotify track URL."""
    try:
        return spotify_url.split('/')[-1]
    except Exception as e:
        cprint(f"Failed to extract track ID: {e}", "red", attrs=["bold"])
        return None


def print_spotiwave():
    ascii_art = """
  .--.--.                           ___                     .---.                             
 /  /    '. ,-.----.              ,--.'|_    ,--,          /. ./|                             
|  :  /`. / \    /  \    ,---.    |  | :,' ,--.'|      .--'.  ' ;                             
;  |  |--`  |   :    |  '   ,'\   :  : ' : |  |,      /__./ \ : |               .---.         
|  :  ;_    |   | .\ : /   /   |.;__,'  /  `--'_  .--'.  '   \' .  ,--.--.    /.  ./|  ,---.  
 \  \    `. .   : |: |.   ; ,. :|  |   |   ,' ,'|/___/ \ |    ' ' /       \ .-' . ' | /     \ 
  `----.   \|   |  \ :'   | |: ::__,'| :   '  | |;   \  \;      :.--.  .-. /___/ \: |/    /  |
  __ \  \  ||   : .  |'   | .; :  '  : |__ |  | : \   ;  `      | \__\/: . .   \  ' .    ' / |
 /  /`--'  /:     |`-'|   :    |  |  | '.'|'  : |__.   \    .\  ; ," .--.; |\   \   '   ;   /|
'--'.     / :   : :    \   \  /   ;  :    ;|  | '.'|\   \   ' \ |/  /  ,.  | \   \  '   |  / |
  `--'---'  |   | :     `----'    |  ,   / ;  :    ; :   '  |--";  :   .'   \ \   \ |   :    |
            `---'.|                ---`-'  |  ,   /   \   \ ;   |  ,     .-./  '---" \   \  / 
              `---`                         ---`-'     '---"     `--`---'             `----'  
"""
    cprint(ascii_art, "green", attrs=["bold"])


def start_wave():

    cprint("Spotify Code Downloader", "green", attrs=["bold"])
    cprint("This program downloads the Spotify code of the currently playing track to your desktop.", "yellow")
    spotify_object = get_spotify_object()

    if not spotify_object:
        cprint("Exiting program due to failed Spotify authentication.", "red", attrs=["bold"])
        return

    cprint("Successfully authenticated with Spotify.", "green", attrs=["bold"])
    external_urls = None
    last_refresh_time = time.time()

    def refresh_token():
        nonlocal spotify_object, last_refresh_time
        if time.time() - last_refresh_time > TOKEN_REFRESH_INTERVAL:
            try:
                cprint("Refreshing access token...", "yellow")
                spotify_object = get_spotify_object()
                if spotify_object:
                    cprint("Successfully refreshed access token.", "green", attrs=["bold"])
                    last_refresh_time = time.time()
                else:
                    cprint("Failed to refresh access token.", "red", attrs=["bold"])
            except Exception as e:
                cprint(f"Error refreshing token: {e}", "red", attrs=["bold"])

    def handle_currently_playing():
        nonlocal external_urls
        try:
            current = spotify_object.currently_playing()
            if not current:
                return

            if current.get('currently_playing_type') == 'ad':
                time.sleep(30)  # Wait for the ad to finish
            else:
                new_external_urls = current['item']['external_urls']
                if new_external_urls != external_urls:
                    external_urls = new_external_urls
                    track_url = external_urls['spotify']
                    track_id = extract_track_id(track_url)
                    album_cover = current['item']['album']['images'][0]['url']
                    if track_id:
                        image_url = f"{BASE_IMAGE_URL}{track_id}"
                        artist_name = current['item']['artists'][0]['name']
                        track_name = current['item']['name']
                        cprint(f"New track detected: {artist_name} - {track_name}. Downloading image from {image_url}",
                               "blue",
                               attrs=["bold"])
                        download_image(image_url, SAVE_PATH)
                        download_image(album_cover, os.path.expanduser("~/Desktop/spotify_album_cover.png"))
        except Exception as e:
            cprint(f"Error handling currently playing track: {e}", "red", attrs=["bold"])

    while True:
        refresh_token()
        handle_currently_playing()
        time.sleep(5)  #Wait for a short period before checking again