import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from model.fetch_details import *

CREDENTIALS_JSON = 'authorization.json'
PLAYLISTS_JSON = 'playlists_bjork_me.json'


# Spotify init with credentials
def init_spotipy(credentials_json):
    """Load credentials from JSON into Spotify client manager and start a session."""
    print('Starting session.')
    credentials = json.load(open(credentials_json))  # 'authorization.json'))
    client_id = credentials['client_id']
    client_secret = credentials['client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotipy_client = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    print('...')
    pl_idx = int(input('Which playlist to make CSV? 0 for Bjork, 1 for mine.'))  # 0 bjork, 1 mine
    return spotipy_client, pl_idx


sp_client, PL_IDX = init_spotipy(CREDENTIALS_JSON)
print('\n...\n')
results_tracks, is_bjork_inspo = get_playlists_data(sp_client, PLAYLISTS_JSON, PL_IDX)
tracks_data = map_track_details(results_tracks, is_bjork_inspo)
tracks_df = features_to_frame(sp_client, tracks_data['id'])
tracks_df_merged = merge_data(tracks_df, tracks_data)
tracks_analyzed_df = get_analyses(sp_client, tracks_df_merged)

print(tracks_analyzed_df.tail(5))

save_details_to_csv(tracks_analyzed_df, PL_IDX)

print('Al dente!')
