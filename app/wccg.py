import re
import string
import subprocess


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

    wccg_proc = subprocess.Popen(['wccg', '-showsem', '-showall', '/english'],
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL,
                                 universal_newlines=True)
    sentence = re.sub(f'[{re.escape(string.punctuation)}]', '', sentence).lower()
    response = wccg_proc.communicate(input=sentence)[0]
    return _as_dict(response or f'"{sentence}": Unable to parse. wccg returned an empty response.')

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
            key = line.split(':')[1].strip()
            parses[key] = []
        elif line:
            parses[key].append(line.strip())

    for key, parse in parses.items():
        parses[key] = ' '.join(parse)

    return dict(sentence=sentence[1:-1],
                number=num_parses,
                parses=parses,
                http_status=200)
