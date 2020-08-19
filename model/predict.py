from model.model import return_predictable_data, request_training


def make_prediction(trained_model, X_test):
    """Using entered data with our trained model to return prediction."""
    knn_prediction = trained_model.predict(X_test)
    return knn_prediction


def displayable_prediction(songs, trained):
    """Modify the datasets with track predictions for display, prints then returns it back."""
    songs['prediction'] = trained
    songs.sort_values('title').head()
    final_prediction = songs[['title', 'is_bjork_inspo', 'prediction']]
    # print(final_prediction)
    return final_prediction


def get_predictions(trained_model):
    """Gets formatted data and uses our trained model, returns predictions in displayable format."""
    X_test, songs = return_predictable_data()
    final_predictions = make_prediction(trained_model, X_test)
    display_pred_df = displayable_prediction(songs, final_predictions)
    return display_pred_df
