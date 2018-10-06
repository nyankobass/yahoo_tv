"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""
from typing import List

from yahoo_tv.program_data import ProgramData


class Schedule:
    def __init__(self, station_list: List[str], program_data_list: List[ProgramData]):
        self.__station_list = station_list
        self.__program_data_list = program_data_list

    def get_all_station(self):
        return self.__station_list.copy()

    def get_prgrams(self, station_name: str):
        if not any(station == station_name for station in self.__station_list):
            return None

        ch_num = self.__station_list.index(station_name) - 1

        programs = filter(lambda n: n.ch_num ==
                          ch_num, self.__program_data_list)

        return programs
