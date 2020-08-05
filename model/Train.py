from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

# import joblib


PLAYLIST_BJORK_CSV = 'playlist_0.csv'
PLAYLIST_ME_CSV = 'playlist_1.csv'
PLS = [PLAYLIST_BJORK_CSV, PLAYLIST_ME_CSV]


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
    songs = songs.drop(['id', 'artist', 'all_artists', 'album'], axis=1)
    prediction = songs.drop(['title'], axis=1)
    return songs, prediction


def split_x_y(songs, prediction):
    """Splits our dataframes into x / y train / test to return and displays snippet."""
    print('Splitting train and test sets...')
    X_train = prediction.drop('is_bjork_inspo', axis=1)
    X_test = songs.drop(['is_bjork_inspo', 'title'], axis=1)
    y_train = prediction['is_bjork_inspo']
    y_test = songs['is_bjork_inspo']
    return X_train, X_test, y_train, y_test


def train_models(X_train, X_test, y_train, y_test):
    """Trains model to return predictions with LogisticRegression and KNeighborsClassifier."""
    print('Training our models!')
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    print('LogisticRegression')
    print(confusion_matrix(y_test, lr_pred))
    print('\n')
    print(classification_report(y_test, lr_pred))
    # Check performance using accuracy
    print(accuracy_score(y_test, lr_pred))
    # Check performance using roc
    roc_auc_score(y_test, lr_pred)
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)
    knn_pred = knn_model.predict(X_test)
    print('KNeighborsClassifier')
    print(confusion_matrix(y_test, knn_pred))
    print('\n')
    print(classification_report(y_test, knn_pred))
    # Check performance using accuracy
    print(accuracy_score(y_test, knn_pred))
    # Check performance using roc
    roc_auc_score(y_test, knn_pred)
    return knn_pred
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    # dt = DecisionTreeClassifier().fit(x_train, y_train)
    # preds = dt.predict(x_test)
    #
    # accuracy = accuracy_score(y_test, preds)
    # joblib.dump(dt, 'playlist-model.model')
    # print('Model Training Finished.\n\tAccuracy obtained: {}'.format(accuracy))
    # return accuracy


def load_dfs():
    """Helper driver function to get in our data for modeling."""
    print('Get our data and make it usable.')
    all_songs_df = get_songs_frame(PLS)
    trainable, prediction = clean(all_songs_df)
    return trainable, prediction


def main():
    """The main event. Gets a prediction: will you be as inspired as Bjork could be!?"""
    print('START!')
    songs, prediction = load_dfs()
    X_train, X_test, y_train, y_test = split_x_y(songs, prediction)
    lr_pred = train_models(X_train, X_test, y_train, y_test)
    songs['prediction'] = lr_pred
    songs.sort_values('title').head()
    final_prediction = songs[['title', 'is_bjork_inspo', 'prediction']]
    # print(final_prediction)
    return final_prediction
