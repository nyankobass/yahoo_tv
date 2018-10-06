"""
parser.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""
import datetime
import re

import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Tag

from yahoo_tv.html import Html
from yahoo_tv.program_data import ProgramData
from yahoo_tv.schedule import Schedule


class Parser:
    def __init__(self, pref_code: int, start_date_time: datetime.datetime = datetime.datetime.today(), chromedriver_path: str = None):
        self.pref_code = pref_code
        self.start_date_time = start_date_time
        self.chromedriver_path = chromedriver_path

        self.schedule = None

    def run(self):
        html = self.__get_html()
        html = self.__delete_wbr(html)

        if html == "":
            return

        station_list, program_data_list = self.parse(html)
        self.schedule = Schedule(station_list, program_data_list)

    def parse(self, html: str):
        soup = BeautifulSoup(html, "html.parser")
        table_soup_list = soup.find_all("table", class_=re.compile("channel"))

        if len(table_soup_list) != 2:
            return

        station_table_soup = table_soup_list[0]
        schedule_table_soup = table_soup_list[1]

        program_data_list = self.__program_analyze((schedule_table_soup))
        station_list = self.__channel_analyze((station_table_soup))

        return station_list, program_data_list

    def get_schedule(self):
        return self.schedule

    def __channel_analyze(self, station_table_soup: Tag):
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

    def __program_analyze(self, program_table_soup: Tag):
        program_soup_list = program_table_soup.find_all(
            "span", attrs={"class", "detail"})

        program_data_list = []
        for program_soup in program_soup_list:
            program_data = self.__get_program_data((program_soup))

            if program_data == None:
                continue

            program_data_list.append(program_data)

        return program_data_list

    def __get_program_data(self, program_soup: Tag):
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
            ch_num = int(pos[1])
        except:
            return None

        time = time_soup.string
        title = title_soup.string

        program_data = ProgramData(time, title, ch_num)

        return program_data

    def __delete_wbr(self, html: str):
        result = html.replace("<wbr />", "").replace("<wbr/>", "")

        return result

    def __get_html(self):
        url = self.__create_url()

        html = Html(chromedriver_path=self.chromedriver_path)

        html.get(url)

        return html.page_source

    def __create_url(self):
        ROW_URL = r"https://tv.yahoo.co.jp/listings/?&va=24&vb=0&vc=0&vd=0&ve=0"

        url = ROW_URL + "&a=" + \
            str(self.pref_code) + "&st=" + str(self.start_date_time.hour)

        return url
