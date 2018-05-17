"""
discopal.py

Find all songs in a Spotify playlist, and create a playlist with all the albums they're from.
"""
import argparse
import time

import spotipy
import spotipy.util

import credentials

def create_spotipy_instance(args):
    scope = "playlist-modify-private"
    authToken = spotipy.util.prompt_for_user_token(args.username, 
        scope, 
        client_id=credentials.SPOTIPY_CLIENT_ID, 
        client_secret=credentials.SPOTIPY_CLIENT_SECRET, 
        redirect_uri=credentials.SPOTIPY_REDIRECT_URI)
    if authToken:
        sp = spotipy.Spotify(auth=authToken)
        return sp
        
    else:
        print("Couldn't get authentication token for " + args.username)
        return None

def get_playlist_albums(sp, args):
    playlist = sp.user_playlist(args.username, args.playlist)
    tracks = playlist['tracks']
    albumUris = [track['track']['album']['uri'] for track in tracks['items']]

    while tracks['next']:
        tracks = sp.next(tracks)
        albumUris.extend([track['track']['album']['uri'] for track in tracks['items']])
    
    # Eliminate duplicates:
    return list(set(albumUris))

def add_album_to_playlist(sp, args, playlistUri, albumUri):
    albumTracks = sp.album_tracks(albumUri)
    songUris = [track['uri'] for track in albumTracks['items']]
    sp.user_playlist_add_tracks(args.username, playlistUri, songUris)

def main():
    parser = argparse.ArgumentParser(prog="discopal", description="Find all songs in a Spotify playlist, and create a playlist with all the albums they're from..")
    parser.add_argument("--username", required=True, help="Your Spotify username.")
    parser.add_argument("--playlist", required=True, help="The playlist to gather artists from.")
    args = parser.parse_args()

    sp = create_spotipy_instance(args)    
    albums = get_playlist_albums(sp, args)
    playlistUri = sp.user_playlist_create(args.username, "Discopal Collection", public=False)['uri']

    for album in albums:
        if album is None:
            continue
        add_album_to_playlist(sp, args, playlistUri, album)

    print("Playlist successfully created!")

if __name__ == '__main__':
    main()