# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://bitbucket.org/ned/coveragepy/src/default/NOTICE.txt

"""Tests of miscellaneous stuff."""

import sys

import coverage

from tests.coveragetest import CoverageTest


class SetupPyTest(CoverageTest):
    """Tests of setup.py"""

    run_in_temp_dir = False

    def setUp(self):
        super(SetupPyTest, self).setUp()
        # Force the most restrictive interpretation.
        self.set_environ('LC_ALL', 'C')

    def test_metadata(self):
        status, output = self.run_command_status(
            "python setup.py --description --version --url --author"
            )
        self.assertEqual(status, 0)
        out = output.splitlines()
        self.assertIn("measurement", out[0])
        self.assertEqual(out[1], coverage.__version__)
        self.assertEqual(out[2], coverage.__url__)
        self.assertIn("Ned Batchelder", out[3])

    def test_more_metadata(self):
        # Let's be sure we pick up our own setup.py
        # CoverageTest restores the original sys.path for us.
        sys.path.insert(0, '')
        from setup import setup_args

        classifiers = setup_args['classifiers']
        self.assertGreater(len(classifiers), 7)
        self.assert_starts_with(classifiers[-1], "Development Status ::")

        long_description = setup_args['long_description'].splitlines()
        self.assertGreater(len(long_description), 7)
        self.assertNotEqual(long_description[0].strip(), "")
        self.assertNotEqual(long_description[-1].strip(), "")
