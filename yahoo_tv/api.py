"""
requests.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

from yahoo_tv.parser import Parser


class API:
    """Yahoo TV API"""

    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path

    def get_schedule(self, pref_code):
        parser = Parser(pref_code, chromedriver_path=self.chromedriver_path)
        parser.run()
        schedule = parser.get_schedule()

        return schedule
