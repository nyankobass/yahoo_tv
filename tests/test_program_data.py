"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import unittest
import datetime

from yahoo_tv.program_data import ProgramData


class TestProgramData(unittest.TestCase):
    """test class of program_data.py
    """

    def test_format(self):
        """test method for format
        """
        test_patterns = [
            ("%t - %dt - %s", "%Y-%m-%d %H:%M:%S",
             "NHKニュース7 - 2018-10-08 19:00:00 - NHK"),
            ("", "%Y-%m-%d %H:%M:%S",
             ""),
            ("%dt\t%t\t%s", "",
             "\tNHKニュース7\tNHK"),
            ("", "", "")
        ]

        program = ProgramData(
            time=datetime.datetime.strptime(
                "2018-10-08 19:00:00", "%Y-%m-%d %H:%M:%S"),
            title="NHKニュース7",
            station="NHK")

        for format, dt_format, expected in test_patterns:
            with self.subTest(format=format, dt_format=dt_format):
                actual = program.format(format=format, dt_format=dt_format)
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(exit=False)
