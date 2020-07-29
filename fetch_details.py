import numpy as np
import pandas as pd
from pandas.core.common import flatten
import json

# Functions


# Playlist data
def get_playlists_data(sp, playlists_json):
    """Load JSON list of playlists and fetch tracks data from Spotify."""
    playlist_index = 0
    playlists = json.load(open(playlists_json))
    playlist_uri = playlists[playlist_index]['uri']
    bjork_inspo = playlists[playlist_index]['bjork_inspo']
    uri = playlist_uri    # the URI is split by ':' to get the username and playlist ID
    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]
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
    return tracks


# Tracks data
def map_track_details(playlist_tracks_data):
    """Maps attributes for tracks from playlists query results."""
    tracks_data = {}
    playlist_tracks_id = []
    playlist_tracks_uri = []
    playlist_tracks_titles = []
    playlist_tracks_artists = []
    playlist_tracks_first_artists = []
    playlist_tracks_albums = []

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

    tracks_data['id'] = playlist_tracks_id
    tracks_data['title'] = playlist_tracks_titles
    tracks_data['artists'] = playlist_tracks_artists
    tracks_data['first_artist'] = playlist_tracks_first_artists
    return tracks_data


# Audio features extraction 
def features_to_frame(sp, tracks_id):
    """Uses Spotify function to extract audio features and returns merged dataframe."""
    features = list(map(lambda x: sp.audio_features(x), tracks_id))
    keys = features[0][0].keys()
    feats = []
    for f in features:
        # idx = f[0].get('id')
        feats.append(f[0])
    features_df = pd.DataFrame(data=feats, columns=keys)
    return features_df


# Merge track infos into single dataframe
def merge_data(features_df, tracks_data):
    features_df['title'] = tracks_data['title']
    features_df['first_artist'] = tracks_data['first_artist']
    features_df['all_artists'] = tracks_data['artists']
    # features_df = features_df.set_index('id')
    features_df = features_df[['id', 'title', 'first_artist', 'all_artists',
                            'danceability', 'energy', 'key', 'loudness',
                            'mode', 'speechiness', 'acousticness',
                            'instrumentalness', 'liveness', 'valence',
                            'tempo', 'duration_ms', 'time_signature']]
    return features_df
