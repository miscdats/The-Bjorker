from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

PLAYLIST_BJORK_CSV = 'playlist_0.csv'
PLAYLIST_ME_CSV = 'playlist_1.csv'
PLS = [PLAYLIST_BJORK_CSV, PLAYLIST_ME_CSV]


def get_songs_frame(playlists):
    """Returns dataframe of songs info from list of playlist CSVs."""
    songs_df = pd.concat(map(pd.read_csv, playlists))
    songs_df.reset_index(drop=True, inplace=True)
    songs_df.drop('Unnamed: 0', 1, inplace=True)
    return songs_df


def clean(songs_df):
    songs_df = songs_df.drop(['id', 'first_artist', 'all_artists', 'album'], axis=1)
    return songs_df


def train_model(songs_df):
    """Trains model."""
    x = songs_df.iloc[:, :-1].values  # X stores features
    y = songs_df.iloc[:, -1].values  # y stores target

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    dt = DecisionTreeClassifier().fit(x_train, y_train)
    preds = dt.predict(x_test)

    accuracy = accuracy_score(y_test, preds)
    joblib.dump(dt, 'playlist-model.model')
    print('Model Training Finished.\n\tAccuracy obtained: {}'.format(accuracy))


all_songs_df = get_songs_frame(PLS)


trainable_df = clean(all_songs_df)
