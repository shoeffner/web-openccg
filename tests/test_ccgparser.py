import json
import unittest

from pathlib import Path

# Shortcut to discover files inside the app instead of making it an installable
# package.
import os
os.sys.path.append(Path(__file__).parent / '..' / 'app')


import ccgparser


class CCGtoJSONTestCase(unittest.TestCase):

    def setUp(self):
        self.test_pairs_path = Path(os.path.dirname(__file__)) / 'test_pairs_ccg_json'
        self.test_directories = list(self.test_pairs_path.glob('*'))
        self.sentence_counter = 0

    def test_ccg_to_json(self):
        """
        Provides some example OpenCCG outputs and the expected JSON parses.
        """
        for directory in self.test_directories:
            with self.subTest(sentence=directory.name):
                for ccg_file in directory.glob('*.ccg'):
                    test_case = ccg_file.name
                    with self.subTest(test_case=test_case):
                        ccg = ccg_file.read_text()
                        expected = json.loads(ccg_file.with_suffix('.json').read_text())

                        actual = ccgparser.ccg_to_json(ccg)

                        self.assertEqual(expected, actual)

