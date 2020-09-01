import os
import pandas as pd
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

DIRT = os.path.dirname(__file__)
FOLDERS = '/app/src/model/'
PLAYLIST_BJORK_CSV = os.path.join(DIRT, FOLDERS, 'playlist_0.csv')  # size : 174
PLAYLIST_ENTERED_CSV = os.path.join(DIRT, FOLDERS, 'playlist_1.csv')
PLS = [PLAYLIST_BJORK_CSV, PLAYLIST_ENTERED_CSV]


def get_songs_frame(playlists):
    """Returns dataframe of songs info from list of playlist CSVs."""
    print('Reading in CSV files...')

    songs_df = pd.concat(map(pd.read_csv, playlists))
    songs_df.reset_index(drop=True, inplace=True)
    songs_df.drop('Unnamed: 0', 1, inplace=True)

    return songs_df


def rescale(songs_df):
    """Rescales features loaded in from spotipy API."""
    print('Rescaling audio features...')

    scaler = StandardScaler()
    features = [['danceability', 'energy', 'key', 'loudness', 'speechiness',
                 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                 'duration_ms', 'time_signature', 'num_bars', 'num_sections',
                 'num_segments']]
    for feature in features:
        songs_df[feature] = scaler.fit_transform(songs_df[feature])

    return songs_df


def clean(songs_df):
    """Normalize data for modeling by setting values and dropping columns (id, artist, all_artists, album)."""
    print('Transforming data to be used...')

    inspo_df = songs_df.loc[songs_df['is_bjork_inspo'] == True].copy()
    songz_df = songs_df.loc[songs_df['is_bjork_inspo'] == False].copy()
    inspo_df['is_bjork_inspo'] = np.ones((len(inspo_df), 1), dtype=int)
    songz_df['is_bjork_inspo'] = np.zeros((len(songz_df), 1), dtype=int)
    songs = inspo_df.append(songz_df, ignore_index=False)
    songs = songs.drop_duplicates()
    songs = rescale(songs)
    songs = songs.drop(['id', 'all_artists', 'album'], axis=1)
    prediction = songs.drop(['title', 'artist'], axis=1)

    return songs, prediction


def split_x_y(songs, prediction):
    """Splits our dataframes into x / y train / test to return and displays snippet."""
    print('Splitting train and test sets...')

    X_train = prediction.drop('is_bjork_inspo', axis=1)
    X_test = songs.drop(['is_bjork_inspo', 'title', 'artist'], axis=1)
    y_train = prediction['is_bjork_inspo']
    y_test = songs['is_bjork_inspo']

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """Trains with KNeighborsClassifier model to return and dumps pickle into barrel."""
    print('Training our models!')

    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)
    dump(knn_model)

    return knn_model


def load_dfs():
    """Helper driver function to get in our data for modeling."""
    print('Get our data and make it usable.')

    all_songs_df = get_songs_frame(PLS)
    trainable, predictable = clean(all_songs_df)

    return trainable, predictable


def dump(trained_model):
    """Use pickling to write our Python object model to file for later use."""
    pikleez = os.path.join(DIRT, 'model.pkl')
    pickle.dump(trained_model, open(pikleez, 'wb'))

    print('Pickled model : ', pikleez)


def make_from_scratch():
    """The main event. Loads up data, trains model."""
    print('START from scratch!')

    songs, predictable = load_dfs()
    X_train, X_test, y_train, y_test = split_x_y(songs, predictable)

    return X_train, X_test, y_train, songs


def request_training():
    """Sends data to training."""
    X_train, X_test, y_train, songs = make_from_scratch()
    train_model(X_train, y_train)


def return_predictable_data():
    """Returns split data for predicting."""
    X_train, X_test, y_train, songs = make_from_scratch()
    return X_test, songs
