"""
__main__.api
~~~~~~~~~~~~
:copyright: (c) 2018 by nyankobass.
:license: MIT, see LICENSE for more details.
"""

import click
import yahoo_tv


@click.command()
@click.option("--pref-code", "-p", type=int, help="都道府県番号", required=True, default=35)
@click.option("--station-list", is_flag=True, help="放送局一覧を表示する")
@click.option("--station", "-s", type=str, help="放送局名")
@click.option("--date", "-d", type=str, help="取得する日(%Y-%m-%d)")
@click.option("--time", "-t", type=int, help="開始時刻(hour)")
@click.option("--chrome", "-c", type=str, help="chromedriver.exeへのPATH")
def main(pref_code, station_list, station, date, time, chrome):
    tv = yahoo_tv.API(chromedriver_path=chrome)
    schedule = tv.get_schedule(pref_code)

    if station_list is True:
        exit_status = show_station_list(schedule)
        return exit_status

    if station is None:
        exit_status = show_all_program(schedule)
        return exit_status

    exit_status = show_programs(schedule, station)
    return exit_status


def show_station_list(schedule: yahoo_tv.schedule.Schedule):
    station_list = schedule.get_all_station()

    if not station_list:
        return 1

    for station in station_list:
        print(station)

    return 0


def show_programs(schedule: yahoo_tv.schedule.Schedule, station: str):
    programs = schedule.get_prgrams(station)

    if not programs:
        return 1

    for program in programs:
        print(program.format())

    return 0


def show_all_program(schedule: yahoo_tv.schedule.Schedule):
    station_list = schedule.get_all_station()

    for station in station_list:
        print("@@ " + station)
        programs = schedule.get_prgrams(station)

        if not programs:
            return 1

        for program in programs:
            print(program.format())

        return 0


if __name__ == "__main__":
    main()
