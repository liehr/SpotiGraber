import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os

# Constants for Spotify API credentials and redirect URI
SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'  # Must be added to the Spotify app settings
SCOPE = "user-read-currently-playing"
TOKEN_REFRESH_INTERVAL = 3600  # Time in seconds

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
    token_info = oauth_object.get_access_token(as_dict=True)
    return spotipy.Spotify(auth=token_info['access_token'])


def download_image(url, save_path):
    """Download an image from the specified URL and save it to the given path."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download image: {e}")


def extract_track_id(spotify_url):
    """Extract the track ID from the Spotify track URL."""
    return spotify_url.split('/')[-1]


def main():
    spotify_object = get_spotify_object()
    external_urls = None
    last_refresh_time = time.time()

    def refresh_token():
        nonlocal spotify_object, last_refresh_time
        if time.time() - last_refresh_time > TOKEN_REFRESH_INTERVAL:
            spotify_object = get_spotify_object()
            last_refresh_time = time.time()

    def handle_currently_playing():
        nonlocal external_urls
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
                image_url = f"{BASE_IMAGE_URL}{track_id}"
                artist_name = current['item']['artists'][0]['name']
                track_name = current['item']['name']
                print(f"New track detected: {artist_name} - {track_name}. Downloading image from {image_url}")
                download_image(image_url, SAVE_PATH)

    while True:
        refresh_token()
        handle_currently_playing()
        time.sleep(5)  # Wait for a short period before checking again


if __name__ == "__main__":
    main()
