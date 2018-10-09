"""
program_data.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import datetime


class ProgramData:
    '''番組データ'''

    def __init__(self, time: datetime.datetime, title: str, station: str):
        ''' コンストラクタ
        :param datetime.datetime time: 開始時刻
        :param str title: 番組タイトル
        :param str staton: 放送局名
        '''
        self.__time = time
        self.__title = title
        self.__station = station

    @property
    def time(self) -> datetime.datetime:
        ''' 開始時刻'''
        return self.__time

    @property
    def title(self) -> str:
        '''番組タイトル'''
        return self.__title

    @property
    def station(self) -> str:
        '''放送局'''
        return self.__station

    def format(self, format: str = "%dt\t%t", dt_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        '''指定されたフォーマットで番組情報をテキスト化する
        使用例：
        format = "%dt - %t - %s"
        return = "2018-10-08 - 19:00:00,NHKニュース7 - NHK"
        :param str format: %dt：開始時刻 %t：番組タイトル %s：放送局
        :param str dt_format: 時刻表示のフォーマット datetimeのフォーマットに従う
        :return str: フォーマットされた文字列
        '''
        text = format.replace(r"%t", self.title)
        text = text.replace(r"%dt", self.time.strftime(dt_format))
        text = text.replace(r"%s", self.station)

        return text
