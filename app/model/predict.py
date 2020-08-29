from .model import return_predictable_data
from .make_dataset import playlist_loader
import json


def make_prediction(trained_model, X_test):
    """Using entered data with our trained model to return prediction."""
    print('Sending trained model to predict...')
    knn_prediction = trained_model.predict(X_test)
    return knn_prediction


def displayable_prediction(songs, trained):
    """Modify the datasets with track predictions for display,
    prints then returns it back."""
    print('Reformatting predicted data for display...')

    final_prediction = songs.copy()
    final_prediction['song'] = songs['artist'].map(str) + ' | ' + songs['title'].map(str)
    final_prediction['inspo?'] = trained
    final_prediction.sort_values('song')
    final_prediction = final_prediction[['song', 'inspo?']]
    readable_feedback = {0: 'Not Quite', 1: 'Would Be'}
    final_prediction['inspo?'] = final_prediction['inspo?'].map(readable_feedback)

    return final_prediction[175:]  # TODO : refactor after form features added/fixed


def get_predictions(trained_model):
    """Called by /predict route path. Gets formatted data and uses our trained model,
    returns predictions in displayable format."""
    print('Getting a call to our model...')

    X_test, songs = return_predictable_data()
    final_predictions = make_prediction(trained_model, X_test)
    display_pred_df = displayable_prediction(songs, final_predictions)

    return display_pred_df


def send_for_analysis(user_playlist_uri):
    """Called by /analyze route path for user input."""
    print('Sending user input for analysis...')

    use_user_provided_uri(user_playlist_uri)
    playlist_loader()


def use_user_provided_uri(user_playlist_uri):
    """Grabs provided URI for Spotify playlist from user input and saves as JSON file
    for predicting on with our model, main use case."""
    json_data = \
        [
            {
                "uri": "spotify:playlist:1VBK0TxoYVEbnfFl6VCtEu",
                "bjork_inspo": True
            },
            {
                "uri": user_playlist_uri,
                "bjork_inspo": False
            }
        ]
    with open('playlists_bjork_me.json', 'w') as json_file:
        json.dump(json_data, json_file)
