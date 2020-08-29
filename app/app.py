import os
import pickle
from rq import Queue
from flask import Flask, request, jsonify, render_template
from .worker import conn
from .app.model.model import request_training
from .app.model.predict import get_predictions, send_for_analysis

app = Flask(__name__)
DIRT = os.path.dirname(__file__)
q = Queue(connection=conn)

model_filename = os.path.join(DIRT, '/app/app/model/model.pkl')
if not os.path.isfile(model_filename):
    request_training()
model = pickle.load(open(model_filename, 'rb'))

# TODO : add 404 page


def get_status(job):
    status = {
        'id': job.id,
        'result': job.result,
        'status': 'failed' if job.is_failed else 'pending' if job.result == None else 'completed'
    }
    status.update(job.meta)
    return status


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    int_features = [x for x in request.form.values()]
    print('User input: ', int_features)

    query_id = request.args.get('job')
    if query_id:
        found_job = q.fetch_job(query_id)
        if found_job:
            output = get_status(found_job)
        else:
            output = {'id': None, 'error_message': 'No job exists with the id number ' + query_id}
    else:
        new_job = q.enqueue(send_for_analysis, int_features[0])
        output = get_status(new_job)

    return render_template('index.html', prediction_text='Analyzing tracks...',
                           column_names=jsonify(output))


@app.route('/predict', methods=['POST'])
def predict():
    # TODO : take in these given values to make_dataset and predict on
    # TODO : make available non-bjork?... new model to train
    output = get_predictions(model)
    # return render_template('index.html', prediction_text='Bjork would be inspired?\n {}'.format(output))
    # link_column is the column that I want to add a button to
    return render_template("index.html", prediction_text='Would Bjork feel inspired from your choices?',
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


@app.route('/.well-known/acme-challenge/kKVx4dguyx1hNIyiGLgiZPqdtLQ9J6D2lEEvBO_uQ7M', methods=['GET'])
def cert():
    out = 'kKVx4dguyx1hNIyiGLgiZPqdtLQ9J6D2lEEvBO_uQ7M'
    return out


if __name__ == "__main__":
    app.run(debug=True)
