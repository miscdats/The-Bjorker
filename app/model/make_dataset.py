import os
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .fetch_details import *


load_dotenv(find_dotenv())
PLAYLISTS_JSON = 'playlists_bjork_me.json'


# Spotify init with credentials
def init_spotipy():
    """Load credentials from JSON into Spotify client manager and start a session."""
    print('Starting spotipy session with secrets.')

    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    pl_idx = 1  # 0 bjork, 1 other

    return spotipy_client, pl_idx


def playlist_loader():
    """Main interface for spotipy use, uses saved URI to analyze tracks!"""
    print('\nPlaylist_loader() in action...\n')

    sp_client, PL_IDX = init_spotipy()
    results_tracks, is_bjork_inspo = get_playlists_data(sp_client, PLAYLISTS_JSON, PL_IDX)
    tracks_data = map_track_details(results_tracks, is_bjork_inspo)
    tracks_df = features_to_frame(sp_client, tracks_data['id'])
    tracks_df_merged = merge_data(tracks_df, tracks_data)
    tracks_analyzed_df = get_analyses(sp_client, tracks_df_merged)

    save_details_to_csv(tracks_analyzed_df, PL_IDX)
    print('Playlist_loader() : Al dente!')
