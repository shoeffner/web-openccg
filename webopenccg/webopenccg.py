import json
import uuid

from flask import (Blueprint,
                   Flask,
                   redirect,
                   render_template,
                   request,
                   url_for)

import graphs
import wccg


bp = Blueprint('openccg', __name__,
               template_folder='templates',
               static_folder='static')


def create_response(sentence, add_graphs=False):
    """Prepares a response.

    Parses the sentence using wccg, then enriches the result with
    some meta data.

    Args:
        sentence: The sentence to parse.
    Returns:
        The response as a dictionary.
    """
    content = wccg.parse(sentence)

    response = {
        'version': '2.3.0',
        'application': 'web-openccg',
        'uuid': str(uuid.uuid4())
    }
    response.update(content)
    if add_graphs:
        try:
            response.update(graphs.create_graphs(content['json_parses']))
        except KeyError:
            pass

    return response


@bp.route('/parse', methods=['POST'])
def parse():
    """Handles parse requests.

    If the requests is a GET request or contains no POST data,
    an error (501 or 400, respectively) is returned.

    Otherwise, the sentence's parse is returned. If wccg was unable to parse
    the sentence, its answer is returned alongside a 422 status code.
    """
    if request.method == 'GET':
        return json.dumps(dict(error="Use POST.", http_status=501)), 501

    if 'sentence' not in request.form:
        try:
            key = next(request.form.keys())
        except StopIteration:
            key = None
    else:
        key = 'sentence'

    # Get sentence from form field or use the first key.
    # The first key could be send e.g. by
    #     curl --data "This is the sentence." 127.0.0.1:5000/parse
    sentence = request.form.get(key) or key
    response = create_response(sentence, 'graphs' in request.args)

    return json.dumps(response), response['http_status']


@bp.route('/use')
def use():
    return render_template('use.html')


@bp.route('/', methods=['GET', 'POST'])
def index():
    """This method shows a minimal user interface."""
    if request.method == 'POST':
        sentence = request.form.get('sentence')
        response = create_response(sentence)
        response = json.dumps(response, indent=4)
    else:
        sentence = None
        response = None
    return render_template('form.html', sentence=sentence, response=response)


app = Flask(__name__)


@app.route('/')
def redirect_to_blueprint():
    return redirect(url_for('openccg.index', **request.args), 308)


@app.route('/parse', methods=['GET', 'POST'])
def redirect_to_parse():
    return redirect(url_for('openccg.parse', **request.args), 308)


app.register_blueprint(bp, url_prefix='/openccg')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
