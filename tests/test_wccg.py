import json
import os
import unittest

from pathlib import Path

from webopenccg import wccg


class CCGtoJSONTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None

    def test_ccg_to_json(self):
        """
        Provides some example OpenCCG outputs and the expected JSON parses.
        """
        test_files = (Path(os.path.dirname(__file__)) / 'test_files' / 'ccg_to_json').glob('*')
        for tf in test_files:
            with self.subTest(test_case=tf.name):
                test_case = json.loads(tf.read_text())
                ccg = test_case['ccg']
                expected = test_case['json']

                self.assertEqual(expected, wccg.ccg_to_json(ccg))
