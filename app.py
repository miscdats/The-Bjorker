import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from fetch_details import *

CREDENTIALS_JSON = 'authorization.json'
PLAYLISTS_JSON = 'playlists_bjork_me.json'

# Spotify init with creds
def init_spotipy(creds_json):
    "Load credentials from JSON into Spotify client manager and start a session."
    credentials = json.load(open(creds_json)) #'authorization.json'))
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp_client


sp_client = init_spotipy(CREDENTIALS_JSON)
results_tracks = get_playlists_data(sp_client, PLAYLISTS_JSON)
tracks_data = map_track_details(results_tracks)
tracks_df = features_to_frame(sp_client, tracks_data['id'])
tracks_df = merge_data(tracks_df, tracks_data)

print(tracks_df.tail())