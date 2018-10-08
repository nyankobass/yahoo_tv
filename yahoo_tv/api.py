"""
requests.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import datetime

from yahoo_tv.parser import Parser
from yahoo_tv.schedule import Schedule


class API:
    """Yahoo TV API"""

    def __init__(self, chromedriver_path: str):
        self.__chromedriver_path = chromedriver_path

    def get_schedule(self, pref_code: int, start_dt: datetime.datetime = datetime.datetime.today()) -> Schedule:
        parser = Parser(pref_code, chromedriver_path=self.__chromedriver_path,
                        start_dt=start_dt)

        exit_status = parser.run()
        if not exit_status:
            return None

        schedule = parser.get_schedule()

        return schedule
