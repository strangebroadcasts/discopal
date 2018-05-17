# DiscoPal
Find all songs in a Spotify playlist, and create a playlist with all the albums they're from.

## Dependencies
The only dependency is [Spotipy](https://github.com/plamere/spotipy). Install it with pip:

`pip3 install spotipy`

## Setup
Since this script requires access to your playlists, you'll have to create a new application at [developer.spotify.com](https://developer.spotify.com/my-applications), and copy the client ID, secret, and redirect URI to *credentials.py*.

## Usage
Pass the username and the Spotify URI of the playlist (found by right-clicking the playlist, and clicking Share -> Copy Spotify URI)

`python3 discopal.py --username example --playlist spotify:user:example:playlist:6F1baSZiDcXm3dqoIlcxjw`

