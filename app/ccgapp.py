import json
import uuid

from flask import Flask, render_template, request

import wccg

app = Flask(__name__)


def create_response(sentence):
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
        'version': '2.1.0',
        'application': 'web-openccg',
        'uuid': str(uuid.uuid4())
    }
    response.update(content)

    return response


@app.route('/parse', methods=['POST'])
def parse():
    """Handles parse requests.

    If the requests is a GET request or contains no POST data,
    an error (501 or 400, respectively) is returned.

    Otherwise, the sentence's parse is returned. If wccg was unable to parse
    the sentence, its answer is returned alongside a 422 status code.
    """
    if request.method == 'GET':
        return json.dumps(dict(error="Use POST.", http_status=501)), 501

    try:
        key = next(request.values.keys())
    except StopIteration:
        key = None

    # Get sentence from form field or use the first key.
    # The first key could be send e.g. by
    #     curl --data "This is the sentence." 127.0.0.1:5000/parse
    sentence = request.form.get(key) or key
    response = create_response(sentence)

    return json.dumps(response), response['http_status']


@app.route('/use')
def use():
    return render_template('use.html')


@app.route('/', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
