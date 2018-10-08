"""
__main__.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""
import sys
import datetime
import click

import yahoo_tv


@click.command()
@click.option("--pref-code", "-p", type=int, help="都道府県番号", default=35)
@click.option("--pref-list", is_flag=True, help="エリア一覧を表示する")
@click.option("--station-list", is_flag=True, help="放送局一覧を表示する")
@click.option("--station", "-s", type=str, help="放送局名")
@click.option("--date", "-d", type=str, help="取得する日(%Y-%m-%d)")
@click.option("--time", "-t", type=int, help="開始時刻(hour)")
@click.option("--chrome", "-c", type=str, help="chromedriver.exeへのPATH")
def main(pref_code, pref_list, station_list, station, date, time, chrome):
    if pref_list:
        exit_status = show_pref_code_list()
        sys.exit(exit_status)

    if not yahoo_tv.API.verify_pref_code(pref_code):
        print("都道府県番号が正しくありません。")
        sys.exit(1)

    today = datetime.datetime.today()

    if date is None:
        dt = today
    else:
        try:
            dt = datetime.datetime.strptime(date + " 4", (r"%Y-%m-%d %H"))
        except:
            print("日付のフォーマットが正しくありません。(%Y-%m-%d)")
            sys.exit(1)

    if not time is None:
        try:
            dt = dt.replace(hour=time)
        except:
            print("時間のフォーマットが正しくありません。(0-23)")
            sys.exit(1)

    if datetime.datetime.today() > dt:
        print("過去の番組表は取得できません。")
        sys.exit(1)

    elif datetime.datetime.today() + datetime.timedelta(weeks=1) < dt:
        print("一週間以上先の番組表は取得できません。")
        sys.exit(1)

    tv = yahoo_tv.API(chromedriver_path=chrome)
    schedule = tv.get_schedule(pref_code, dt)

    if schedule is None:
        print("番組表を取得できませんでした。")
        sys.exit(1)

    if station_list is True:
        exit_status = show_station_list(schedule)
        sys.exit(exit_status)

    if station is None:
        exit_status = show_all_programs(schedule)
        sys.exit(exit_status)

    exit_status = show_programs(schedule, station)
    sys.exit(exit_status)


def show_pref_code_list():
    pref_code_list = yahoo_tv.API.get_pref_code_list()

    for code, name in pref_code_list.items():
        print(str(code) + "\t" + name)

    return 0


def show_station_list(schedule: yahoo_tv.schedule.Schedule):
    station_list = schedule.get_all_station()

    if not station_list:
        print("放送局一覧を取得できませんでした。")
        return 1

    for station in station_list:
        print(station)

    return 0


def show_programs(schedule: yahoo_tv.schedule.Schedule, station: str):
    programs = schedule.get_prgrams(station)

    if not programs:
        print("指定された放送局は存在しません。")
        return 1

    for program in programs:
        print(program.format())

    return 0


def show_all_programs(schedule: yahoo_tv.schedule.Schedule):
    station_list = schedule.get_all_station()

    if not station_list:
        print("放送局一覧を取得できませんでした。")
        return 1

    for station in station_list:
        print("@@ " + station)
        programs = schedule.get_prgrams(station)

        for program in programs:
            print(program.format())

    return 0


if __name__ == "__main__":
    main()
