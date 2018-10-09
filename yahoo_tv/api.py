"""
requests.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import datetime
from typing import Dict

from yahoo_tv.parser import Parser
from yahoo_tv.schedule import Schedule


class API:
    """Yahoo TV API"""

    PREF_NAME_LIST = [
        "北海道（札幌）",
        "北海道（函館）",
        "北海道（旭川）",
        "北海道（帯広）",
        "北海道（釧路）",
        "北海道（北見）",
        "北海道（室蘭）",
        "青森",
        "岩手",
        "宮城",
        "秋田",
        "山形",
        "福島",
        "東京",
        "神奈川",
        "埼玉",
        "千葉",
        "茨城",
        "栃木",
        "群馬",
        "山梨",
        "新潟",
        "長野",
        "富山",
        "石川",
        "福井",
        "愛知",
        "岐阜",
        "静岡",
        "三重",
        "大阪",
        "兵庫",
        "京都",
        "滋賀",
        "奈良",
        "和歌山",
        "鳥取",
        "島根",
        "岡山",
        "広島",
        "山口",
        "徳島",
        "香川",
        "愛媛",
        "高知",
        "福岡",
        "佐賀",
        "長崎",
        "熊本",
        "大分",
        "宮崎",
        "鹿児島",
        "沖縄"
    ]

    def __init__(self, chromedriver_path: str):
        '''コンストラクタ
        :param str chromedriver_path: ChromeDriverへのパス
        '''
        self.__chromedriver_path = chromedriver_path

    @staticmethod
    def get_pref_code_list() -> Dict[int, str]:
        '''都道府県番号と都道府県の対応関係を返す
        :return Dict[int, str]: {都道府県番号: 地域名}形式の辞書データ
        '''
        pref_dict = {}

        key = 10
        for pref_name in API.PREF_NAME_LIST:
            pref_dict[key] = pref_name
            key += 1
        return pref_dict

    @staticmethod
    def verify_pref_code(pref_code: int) -> bool:
        '''都道府県番号が存在するか確認する
        :param int pref_code: 都道府県番号
        :return bool: 存在する場合True
        '''
        min_code = 10
        max_code = 62

        if min_code > pref_code:
            return False

        if max_code < pref_code:
            return False

        return True

    def get_schedule(self, pref_code: int, start_dt: datetime.datetime = datetime.datetime.today()) -> Schedule:
        '''指定された都道府県・日付の番組表を返す
        :param int pref_code: 都道府県番号
        :param datetime.datetime start_dt: 取得したい日付（現在時刻～1週間後）
        :return yahoo_tv.Schedule: 取得された番組表。失敗した場合はNone
        '''
        if not API.__verify_dt(start_dt):
            return None

        parser = Parser(pref_code, chromedriver_path=self.__chromedriver_path,
                        start_dt=start_dt)

        exit_status = parser.run()
        if not exit_status:
            return None

        schedule = parser.get_schedule()

        return schedule

    @staticmethod
    def __verify_dt(dt: datetime.datetime):
        today = datetime.datetime.today()

        if today > dt:
            print("過去の番組表は取得できません。")
            return False

        elif today + datetime.timedelta(weeks=1) < dt:
            print("一週間以上先の番組表は取得できません。")
            return False

        return True
