import os
# import numpy as np
from flask import Flask, request, jsonify, render_template
from .model.model import request_training
from .model.predict import get_predictions
import pickle

app = Flask(__name__)
DIRT = os.path.dirname(__file__)

model_filename = os.path.join(DIRT, '/app/app/model/model.pkl')
if not os.path.isfile(model_filename):
    request_training()
model = pickle.load(open(model_filename, 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    # TODO : take in these given values to make_dataset and predict on
    # TODO : make available non-bjork?... new model to train
    # final_features = [np.array(int_features)]
    # prediction = model.predict(final_features)
    # output = round(prediction[0], 2)

    output = get_predictions(model)

    # return render_template('index.html', prediction_text='Bjork would be inspired?\n {}'.format(output))
    # link_column is the column that I want to add a button to
    return render_template("index.html", prediction_text='Bjork feels... Inspired?',
                           column_names=output.columns.values, row_data=list(output.values.tolist()),
                           zip=zip)  # link_column="Song ID/URI?",


@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    # prediction = model.predict([np.array(list(data.values()))])
    # output = prediction[0]
    # TODO : change these so values given are make_dataset and predict on
    # TODO : train new model if given playlist URI
    # output = get_predictions(model)
    output = ' Hello!'
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
