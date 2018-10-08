"""
parser.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""
from typing import List
import datetime
import re

import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Tag

from yahoo_tv.html import Html
from yahoo_tv.program_data import ProgramData
from yahoo_tv.schedule import Schedule


class Parser:
    def __init__(self, pref_code: int, start_dt: datetime.datetime = datetime.datetime.today(), chromedriver_path: str = None):
        self.__pref_code = pref_code
        self.__start_dt = start_dt
        self.__chromedriver_path = chromedriver_path

        self.__schedule = None

        self.date_offset = 0

    def run(self) -> bool:
        self.date_offset = 0

        html = self.__get_html()
        html = self.__delete_wbr(html)

        if html == "":
            return False

        station_list, program_data_list = self.parse(html)

        if not station_list:
            return False

        if not program_data_list:
            return False

        self.__schedule = Schedule(station_list, program_data_list)

        return True

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        table_soup_list = soup.find_all("table", class_=re.compile("channel"))

        if len(table_soup_list) != 2:
            return [], []

        station_table_soup = table_soup_list[0]
        schedule_table_soup = table_soup_list[1]

        station_list = self.__station_analyze((station_table_soup))
        program_data_list = self.__program_analyze(
            schedule_table_soup, station_list)

        return station_list, program_data_list

    def get_schedule(self) -> Schedule:
        return self.__schedule

    def __station_analyze(self, station_table_soup: Tag) -> List[str]:
        # マルチチャンネル対応
        script = station_table_soup.find_all(class_="slideprogOpenBtn")
        for tag in script:
            tag.extract()

        station_soup_list = station_table_soup.find_all(
            "td", attrs={"class", "station"})

        station_list = []
        for station_soup in station_soup_list:
            station_list.append(station_soup.a.string)

        return station_list

    def __program_analyze(self, program_table_soup: Tag, station_list: List[str]) -> List[ProgramData]:
        program_soup_list = program_table_soup.find_all(
            "span", attrs={"class", "detail"})

        program_data_list = []
        for program_soup in program_soup_list:
            program_data = self.__get_program_data(program_soup, station_list)

            if program_data == None:
                continue

            program_data_list.append(program_data)

        return program_data_list

    def __get_program_data(self, program_soup: Tag, station_list: List[str]) -> ProgramData:
        time_soup = program_soup.find("span", attrs={"class", "time"})
        title_soup = program_soup.find("a", attrs={"class", "title"})

        if time_soup == None:
            return None

        elif title_soup == None:
            return None

        MatchOB = re.search(r"pos:\d", str(title_soup))
        if not MatchOB:
            return None

        pos = MatchOB.group().split(":")
        try:
            ch_pos = int(pos[1])
        except:
            return None

        time = time_soup.string
        title = title_soup.string
        station = station_list[ch_pos - 1]

        program_data = ProgramData(self.__to_datetime(time), title, station)

        return program_data

    def __to_datetime(self, time) -> datetime.datetime:
        time_list = time.split(":")
        hour = int(time_list[0])
        minute = int(time_list[1])

        if hour >= 24:
            hour = hour % 24
            self.date_offset = 1

        return datetime.datetime(
            year=self.__start_dt.year,
            month=self.__start_dt.month,
            day=self.__start_dt.day + self.date_offset,
            hour=hour,
            minute=minute)

    def __delete_wbr(self, html: str) -> str:
        result = html.replace("<wbr />", "").replace("<wbr/>", "")

        return result

    def __get_html(self) -> str:
        url = self.__create_url()

        html = Html(chromedriver_path=self.__chromedriver_path)

        html.get(url)

        return html.page_source

    def __create_url(self) -> str:
        ROW_URL = r"https://tv.yahoo.co.jp/listings/?&va=24&vb=0&vc=0&vd=0&ve=0"

        url = ROW_URL + "&a=" + \
            str(self.__pref_code) + "&st=" + str(self.__start_dt.hour)

        return url
