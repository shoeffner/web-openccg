import json

from flask import Flask, render_template, request, redirect

import wccg

app = Flask(__name__)


def is_non_gui_agent(ua_string):
    """Returns True for a few specific matches for User-Agent strings.

    This is a very simple heuristic to distinguish between browser agents
    and command line or programmatical agents, and the list might grow.

    Returns:
        True if the User-Agent string contains either of a set of possible
        user agents, for example curl/, wget/ or python-requests/.
    """
    uas = ('python-requests/', 'curl/', 'wget/')
    ua_string = ua_string.lower()
    return any(ua in ua_string for ua in uas)


@app.route('/gui', methods=['GET', 'POST'])
def gui():
    """Presents a simple input form to a browser user.
    """
    sentence = request.form.get('sentence')
    response = wccg.parse(sentence)
    response = json.dumps(response, indent=4)
    return render_template('form.html', sentence=sentence, response=response)


@app.route('/', methods=['GET', 'POST'])
def index():
    """This method handles / requests.

    If the request is from a GUI client (that is, is_non_gui_agent is False),
    a redirect to /gui is returned.

    Else, if the requests is a GET request or contains no POST data,
    an error (501 or 400, respectively) is returned.

    Otherwise, the sentence's parse is returned. If wccg was unable to parse
    the sentence, its answer is returned alongside a 422 status code.
    """
    ua = request.headers.get('User-Agent')
    if is_non_gui_agent(ua):
        if request.method == 'GET':
            return json.dumps(dict(error="Use POST.", http_status=501)), 501

        try:
            key = next(request.values.keys())
        except StopIteration:
            key = None

        # Get sentence from form field or use the first key.
        # The first key could be send e.g. by
        #     curl --data "This is the sentence." 127.0.0.1:5000
        sentence = request.form.get(key) or key
        response = wccg.parse(sentence)
        return json.dumps(response), response['http_status']

    return redirect('/gui', code=307)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
