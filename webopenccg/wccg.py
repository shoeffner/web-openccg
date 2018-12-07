import itertools
import os
import re
import string
import subprocess

from tatsu.util import asjson
from tatsu.model import ModelBuilderSemantics

from webopenccg.generated_openccg_parser import OpenCCGParser


def parse(sentence):
    """Parses a sentence using OpenCCG's command line tool wccg.

    Before the sentence is parsed, all (English) punctuation is removed and
    it is converted to lowercase, as the grammar and OpenCCG work best this way.

    Args:
        sentence: The sentence to parse.
    Returns:
        A dictionary containing either the parsed version or an error message.
        The dictionary contains the sentence, an appropriate http_status
        and either an error or the parses.
    """
    if not sentence:
        return dict(error='No sentence provided.', http_status=400)

    wccg_proc = subprocess.Popen(['wccg', '-showsem', '-showall', os.environ.get('GRAMMAR_DIR', '/grammar')],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 universal_newlines=True)
    sentence = re.sub(f'[{re.escape(string.punctuation)}]', '', sentence).lower()
    response = wccg_proc.communicate(input=sentence)[0]

    wccg_response = _as_dict(response or f'"{sentence}": Unable to parse. wccg returned an empty response.')
    wccg_response = jsonify_parses(wccg_response)

    return wccg_response


def ensure_unique_key(new_key, dictionary):
    """If new_key is already in dictionary, a number is appended to new_key.

    If new_key is 'main' and 'main' is already in dictionary, the following keys
    are tried until one is not part of dictionary:

        main/0
        main/1
        main/2
        ...
        main/10
        main/11
        ...


    Args:
        new_key: The key to be added or modified.
        dictionary: The dictionary to check new_key against.
    Returns:
        new_key if the key is unique, otherwise an alternative version.

    >>> keys = ['a', 'a/0', 'a/1', 'a/2', 'a/3']
    >>> ensure_unique_key('a', keys)
    'a/4'
    >>> ensure_unique_key('b', keys)
    'b'
    >>> ensure_unique_key('a/1', keys)
    'a/1/0'
    """
    if new_key not in dictionary:
        return new_key

    for i in itertools.count():
        key = f'{new_key}/{i}'
        if key not in dictionary:
            return key


def _as_dict(response):
    """Converts the response to JSON so it's easier to parse for other
    programs."""
    lines = response.splitlines()
    if ': Unable to' in lines[0]:
        sentence, error = response.split(':', 1)
        error = ' '.join(l.strip() for l in error.splitlines()).strip()
        return dict(sentence=sentence[1:-1], error=error, http_status=422)
    sentence, num_parses = lines[0].split(':')
    num_parses = int(num_parses.split()[0])

    parses = {}
    key = None
    for line in lines[2:]:
        if line.startswith('Parse'):
            key = ensure_unique_key(line.split(':')[1].strip(), parses.keys())
            parses[key] = []
        elif line:
            parses[key].append(line.strip())

    for key, parse in parses.items():
        parses[key] = ' '.join(parse)

    return dict(sentence=sentence[1:-1],
                parses=parses,
                http_status=200)


def jsonify_parses(wccg_response):
    """Converts the OpenCCG responses to proper JSON objects and adds them
    to the supplied dictionary.

    Args:
        wccg_response: The dictionary as returned by _as_dict.
    Returns:
        A copy of the dictionary, additionally containing parses_json.
    """
    json_parses = {}
    for key, parse in wccg_response.get('parses', {}).items():
        json_parses[key] = ccg_to_json(parse)
    copy = wccg_response.copy()
    copy['json_parses'] = json_parses
    return copy


def ccg_to_json(to_parse):
    """Parses an OpenCCG string into a more easily digestiable JSON format.

    Args:
        to_parse: The OpenCCG string.
    Returns:
        A JSON representation of the OpenCCG string.
    """
    return asjson(OpenCCGParser().parse(to_parse,
                                        semantics=ModelBuilderSemantics(),
                                        parseinfo=False))
