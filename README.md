# Spotify Code - Currently Playing Tracker

This project tracks the currently playing song on Spotify and downloads the corresponding scannable image for the track. The image is saved to the user's desktop.

## Features

- Authenticates with Spotify using OAuth.
- Continuously checks the currently playing track.
- Refreshes the Spotify token every 60 minutes.
- Downloads the scannable image for the currently playing track.

## Requirements

- Python 3.x
- `spotipy` library
- `requests` library

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required libraries:
    ```sh
    pip install spotipy requests
    ```

3. Set up your Spotify Developer credentials:
    - Create a Spotify Developer account and create an app.
    - Add `http://localhost:8888/callback` to the Redirect URIs in the Spotify app settings.
    - Replace `YOUR_CLIENT_ID` and `YOUR_CLIENT_SECRET` in `main.py` with your Spotify app credentials.

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. The script will authenticate with Spotify and start tracking the currently playing song. If a new song is detected, it will download the scannable image to your desktop.

## Configuration

- **Spotify API Credentials**: Set your Spotify API credentials in `main.py`.
- **Token Refresh Interval**: The token refresh interval is set to 3600 seconds (60 minutes) by default.
- **Image Save Path**: The image is saved to `~/Desktop/spotify_code.png` by default.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
