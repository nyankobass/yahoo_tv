"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""
from typing import List
import logging

from yahoo_tv.program_data import ProgramData

LOGGER = logging.getLogger(__name__)


class Schedule:
    '''番組表データ'''

    def __init__(self, station_list: List[str], program_data_list: List[ProgramData]):
        '''番組表
        :param List[str] station_list: 放送局一覧
        :param List[ProgramData] program_data_list: 番組一覧
        '''

        self.__station_list = station_list
        self.__program_data_list = program_data_list

    def get_all_station(self):
        '''放送局一覧を取得する
        :return List[str]: 放送局一覧
        '''

        return self.__station_list.copy()

    def get_prgrams(self, station: str) -> List[ProgramData]:
        '''指定された放送局の番組一覧を返す
        :param str station: 放送局
        :return List[ProgramData]: 番組一覧 指定された放送局が存在しなければNone
        '''

        if not any(station == s for s in self.__station_list):
            LOGGER.error("指定された放送局は存在しません。")
            return None

        programs = filter(lambda n: n.station == station,
                          self.__program_data_list)

        return programs
