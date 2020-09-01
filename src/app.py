import os
import pickle
from rq import Queue
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
from src.model.model import request_training
from src.model.predict import send_for_analysis
from src.worker import conn

app = Flask(__name__)

DIRT = os.path.dirname(__file__)
model_filename = os.path.join(DIRT, '/app/src/model/model.pkl')
if not os.path.isfile(model_filename):
    request_training()
model = pickle.load(open(model_filename, 'rb'))

q = Queue(connection=conn)
finished = False


@app.route('/', methods=['GET', 'POST'])
def home():
    """ First page reached, we are home. """
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """ Starts the main processes, activated by button click submission of URI input. """
    if request.method == 'GET':
        return url_for('home')

    elif request.method == 'POST':
        int_features = [x for x in request.form.values()]
        print('User input: ', int_features)

        global finished
        finished = False
        query_id = request.args.get('job')
        if query_id:
            found_job = q.fetch_job(query_id)
            if found_job:
                output = get_status(found_job)
            else:
                output = return_error(query_id)
        else:
            new_job = q.enqueue(send_for_analysis, int_features[0], model)
            output = get_status(new_job)
            query_id = output['data']['job_id']

        query_id = str(query_id)
        print('Init request: ', output)
        print('Query ID: ', query_id)
        # flash('Analyzing {}... sit tight, might take a minute.'.
        #       format(int_features))
        return render_template('loading.html', job_id=query_id)


def get_status(job):
    """ Periodically checked to return updated job status. """
    global finished
    status = {
        "status": "completed",
        "finished": str(finished).lower(),
        "data": {
            'job_id': job.id,  # job.get_id() job.get_status()
            'job_status': 'failed' if job.is_failed else 'pending' if job.result == None else 'completed',
            'job_result': job.result,
        }
    }
    status['data'].update(job.meta)
    print('Get_status: ', status)
    return status


def return_error(job_id):
    """ Returns error message with invalid job_id status. """
    global finished
    res = {
        "status": "error",
        "finished": str(finished).lower(),
        "error_message": 'Job {} not found! '.format(job_id),
        "data": {
            "job_id": None,
            "job_status": "failed"
        }
    }
    print('Return_error: ', res)
    return jsonify(res)


@app.route('/status/<job_id>', methods=['GET'])
def process_status(job_id):
    """ Returns the status of the background process worker for given job. """
    print('Process_status: ', job_id)
    job = q.fetch_job(job_id)
    if job:
        res = get_status(job)
    else:
        res = return_error(job_id)
    return jsonify(res)


@app.route('/results/<job_id>', methods=['GET', 'POST'])
def results(job_id):
    """ Return result of the large process. """
    print('Results for job ID: ', job_id)

    global finished
    if request:
        output = request.get_json(force=True)
    else:
        job = q.fetch_job(job_id)
        output = get_status(job)
    finished = True

    return render_template("index.html",
                           prediction_text='Would Bjork feel inspired from your choices?',
                           column_names=output.result.columns.values,
                           row_data=list(output.result.values.tolist()),
                           zip=zip)  # link_column="Song ID/URI?",
    # TODO : add 404 page
    # TODO : take in these given values to make_dataset and predict on
    # TODO : make available non-bjork?... new model to train
    # return render_template('index.html',
    # prediction_text='Bjork would be inspired?\n {}'.format(output))
    # link_column is the column that I want to add a button to
    # return jsonify(output)


@app.route('/.well-known/acme-challenge/kKVx4dguyx1hNIyiGLgiZPqdtLQ9J6D2lEEvBO_uQ7M',
           methods=['GET'])
def cert():
    """ EFF SSL certification endpoint. """
    # TODO : rerun cert program
    out = 'kKVx4dguyx1hNIyiGLgiZPqdtLQ9J6D2lEEvBO_uQ7M'
    return out


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)
