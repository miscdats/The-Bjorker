from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
# import joblib


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
    """Drop unwanted columns for modeling (id, artist, all_artists, album)."""
    songs_df = songs_df.drop(['id', 'artist', 'all_artists', 'album'], axis=1)
    return songs_df


def split_x_y(songs, prediction):
    """Splits our dataframes into x / y train / test to return and displays snippet."""
    X_train = prediction.drop('is_bjork_inspo', axis=1)
    X_test = songs.drop(['is_bjork_inspo', 'title'], axis=1)
    y_train = prediction['is_bjork_inspo']
    y_test = songs['is_bjork_inspo']

    X_train.head(1)
    X_test.head(1)
    y_train.tail(1)
    y_test.tail(1)
    return X_train, X_test, y_train, y_test


def train_models(X_train, X_test, y_train, y_test):
    """Trains model to return predictions with LogisticRegression and KNeighborsClassifier."""
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    print(confusion_matrix(y_test, lr_pred))
    print('\n')
    print(classification_report(y_test, lr_pred))
    knn_model = KNeighborsClassifier()
    knn_model.fit(X_train, y_train)
    knn_pred = knn_model.predict(X_test)
    print(confusion_matrix(y_test, knn_pred))
    print('\n')
    print(classification_report(y_test, knn_pred))
    return lr_pred
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    # dt = DecisionTreeClassifier().fit(x_train, y_train)
    # preds = dt.predict(x_test)
    #
    # accuracy = accuracy_score(y_test, preds)
    # joblib.dump(dt, 'playlist-model.model')
    # print('Model Training Finished.\n\tAccuracy obtained: {}'.format(accuracy))
    # return accuracy


def load_dfs():
    all_songs_df = get_songs_frame(PLS)
    trainable = clean(all_songs_df)
    prediction = trainable.copy().drop(['title'], axis=1)
    return trainable, prediction


def main():
    songs, prediction = load_dfs()
    X_train, X_test, y_train, y_test = split_x_y(songs, prediction)
    lr_pred = train_models(X_train, X_test, y_train, y_test)
    songs['prediction'] = lr_pred
    songs.sort_values('title').head()
    final_prediction = songs[['title', 'is_bjork_inspo', 'prediction']]
    print(final_prediction)
    # return final_prediction
