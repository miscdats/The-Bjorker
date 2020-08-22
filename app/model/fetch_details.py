import pandas as pd
import json

# Functions


# Playlist data
def get_playlists_data(sp, playlists_json, pl_idx):
    """Load JSON list of playlists and fetch tracks data from Spotify."""
    print('Getting playlist data...')
    playlist_index = pl_idx
    playlists = json.load(open(playlists_json))
    playlist_uri = playlists[playlist_index]['uri']
    is_bjork_inspo = playlists[playlist_index]['bjork_inspo']
    uri = playlist_uri    # the URI is split by ':'
    playlist_id = uri.split(':')[2]
    # call upon our client, get more than 99 tracks
    offset = 0
    tracks = []
    fields = 'items(track(id,name,artists(name),album(name),uri))'  # query these from Track object
    while True:
        response = sp.playlist_tracks(playlist_id=playlist_id, offset=offset, fields=fields, additional_types=['track'])
        tracks.extend(response['items'])
        offset = offset + len(response['items'])
        if len(response['items']) == 0:
            break
    return tracks, is_bjork_inspo


# Tracks data
def map_track_details(playlist_tracks_data, is_bjork_inspo):
    """Maps attributes for tracks from playlists query results."""
    print('Mapping track details...')
    tracks_data = {}
    playlist_tracks_id = []
    playlist_tracks_uri = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_albums = []
    playlist_bjork_inspo = []

    for track in playlist_tracks_data:
        track = track.get('track')
        playlist_tracks_id.append(track.get('id'))
        # playlist_tracks_uri.extend(track['uri'])
        playlist_tracks_albums.append(track.get('album').get('name'))
        playlist_tracks_titles.append(track.get('name'))
        # list all artists credited
        artist_list = []
        for artist in track.get('artists'):
            artist_list.append(artist.get('name'))
        playlist_tracks_artists.append(artist_list)
        playlist_tracks_first_artists.append(artist_list[0])
        playlist_bjork_inspo.append(is_bjork_inspo)

    tracks_data['id'] = playlist_tracks_id
    tracks_data['title'] = playlist_tracks_titles
    tracks_data['artists'] = playlist_tracks_artists
    tracks_data['first_artist'] = playlist_tracks_first_artists
    tracks_data['album'] = playlist_tracks_albums
    tracks_data['is_bjork_inspo'] = playlist_bjork_inspo
    return tracks_data


# Audio features extraction 
def features_to_frame(sp, tracks_id):
    """Uses Spotify function to extract audio features and returns merged dataframe."""
    print('Putting features in dataframe...')
    features = list(map(lambda x: sp.audio_features(x), tracks_id))
    keys = features[0][0].keys()
    feats = []
    for f in features:
        feats.append(f[0])
    features_df = pd.DataFrame(data=feats, columns=keys)
    return features_df


# Merge track infos into single dataframe
def merge_data(features_df, tracks_data):
    """Cleans up and merges track data into single dataframe."""
    print('Merging all data so far...')
    features_df['title'] = tracks_data['title']
    features_df['artist'] = tracks_data['first_artist']
    features_df['all_artists'] = tracks_data['artists']
    features_df['album'] = tracks_data['album']
    features_df['is_bjork_inspo'] = tracks_data['is_bjork_inspo']
    # features_df = features_df.set_index('id')
    features_df = features_df[['id', 'is_bjork_inspo', 'title', 'artist', 'album', 'all_artists',
                               'danceability', 'energy', 'key', 'loudness',
                               'mode', 'speechiness', 'acousticness',
                               'instrumentalness', 'liveness', 'valence',
                               'tempo', 'duration_ms', 'time_signature']].copy()
    return features_df


# Merge analysis info to dataframe
def get_analyses(sp, features_df):
    """Use Spotipy to get audio analysis for each track in dataframe, added as columns."""
    print('Analyze this!')
    num_bars = []
    num_sections = []
    num_segments = []

    for i in range(0, len(features_df['id'])):
        analysis = sp.audio_analysis(features_df.iloc[i]['id'])
        num_bars.append(len(analysis['bars']))  # beats/time_signature
        num_sections.append(len(analysis['sections']))
        num_segments.append(len(analysis['segments']))

    features_df['num_bars'] = num_bars
    features_df['num_sections'] = num_sections
    features_df['num_segments'] = num_segments

    return features_df


def save_details_to_csv(features_df, playlist_index):
    csv_filename = "playlist_" + str(playlist_index) + ".csv"
    print('\nSaving details to : ', csv_filename)
    features_df.to_csv(csv_filename, encoding='utf-8', index="false")
