import json
import unittest

from pathlib import Path

# Shortcut to discover files inside the app instead of making it an installable
# package.
import os
os.sys.path.append(Path(__file__).parent / '..' / 'app')


import ccgparser  # noqa


class CCGtoJSONTestCase(unittest.TestCase):

    def test_ccg_to_json(self):
        """
        Provides some example OpenCCG outputs and the expected JSON parses.
        """
        self.test_files = (Path(os.path.dirname(__file__))
                           / 'test_files'
                           / 'ccg_to_json').glob('*')

        for name, test_case in [(tf.name, json.loads(tf.read_text()))
                                for tf in self.test_files]:
            with self.subTest(test_case=name):
                ccg = test_case['ccg']
                expected = test_case['json']

                self.assertEqual(expected, ccgparser.ccg_to_json(ccg))
