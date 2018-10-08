"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import datetime


class ProgramData:
    def __init__(self, time: datetime.datetime, title: str, station: str):
        self.__time = time
        self.__title = title
        self.__station = station

    @property
    def time(self) -> datetime.datetime:
        return self.__time

    @property
    def title(self) -> str:
        return self.__title

    @property
    def station(self) -> str:
        return self.__station

    def format(self, format: str = "%dt\t%t", dt_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        text = format.replace(r"%t", self.title)
        text = text.replace(r"%dt", self.time.strftime(dt_format))
        text = text.replace(r"%s", self.station)

        return text
