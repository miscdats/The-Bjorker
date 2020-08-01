from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import pandas as pd

PLAYLIST_CSV = 'playlist_0.csv'


def train_model(playlist_csv):
    playlist_df = pd.read_csv(playlist_csv)

    x = playlist_df.iloc[:, :-1].values  # X stores features
    y = playlist_df.iloc[:, -1].values  # y stores target

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)
    dt = DecisionTreeClassifier().fit(x_train, y_train)
    preds = dt.predict(x_test)

    accuracy = accuracy_score(y_test, preds)
    joblib.dump(dt, 'playlist-model.model')
    print('Model Training Finished.\n\tAccuracy obtained: {}'.format(accuracy))
