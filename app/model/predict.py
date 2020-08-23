from .model import return_predictable_data


def make_prediction(trained_model, X_test):
    """Using entered data with our trained model to return prediction."""
    knn_prediction = trained_model.predict(X_test)
    return knn_prediction


def displayable_prediction(songs, trained):
    """Modify the datasets with track predictions for display, prints then returns it back."""
    final_prediction = songs.copy()
    final_prediction['song'] = songs['artist'].map(str) + ' - ' + songs['title'].map(str)
    final_prediction['inspo?'] = trained
    final_prediction.sort_values('song')
    final_prediction = final_prediction[['song', 'inspo?']]
    readable_feedback = {0: 'Not Quite', 1: 'Would Be'}
    final_prediction['inspo?'] = final_prediction['inspo?'].map(readable_feedback)
    return final_prediction[175:]  # TODO : refactor after form feature added/fixed


def get_predictions(trained_model):
    """Gets formatted data and uses our trained model, returns predictions in displayable format."""
    X_test, songs = return_predictable_data()
    final_predictions = make_prediction(trained_model, X_test)
    display_pred_df = displayable_prediction(songs, final_predictions)
    return display_pred_df
