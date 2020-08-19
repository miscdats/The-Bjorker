from model.model import return_predictable_data, request_training


def make_prediction(trained_model, X_test):
    """Using entered data with our trained model to return prediction."""
    knn_prediction = trained_model.predict(X_test)
    return knn_prediction


def displayable_prediction(songs, trained):
    """Modify the datasets with track predictions for display, prints then returns it back."""
    final_prediction = songs.copy()
    final_prediction['prediction'] = trained
    final_prediction.sort_values('title')
    final_prediction = final_prediction[['title', 'artist', 'prediction']]
    readable_feedback = {0: 'Not Quite', 1: 'Would Like'}
    final_prediction['prediction'] = final_prediction['prediction'].map(readable_feedback)
    # final_prediction = final_prediction.iloc[175:]
    # print(final_prediction)
    return final_prediction[175:]


def get_predictions(trained_model):
    """Gets formatted data and uses our trained model, returns predictions in displayable format."""
    X_test, songs = return_predictable_data()
    final_predictions = make_prediction(trained_model, X_test)
    display_pred_df = displayable_prediction(songs, final_predictions)
    return display_pred_df
