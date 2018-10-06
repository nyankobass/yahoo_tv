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
@click.option("--chrome", type=str, help="chromedriver.exeへのPATH")
def main(pref_code, station_list, station, chrome):
    print(chrome)

    tv = yahoo_tv.API(chromedriver_path=chrome)

    schedule = tv.get_schedule(pref_code)

    if station_list is True:
        station_list = schedule.get_all_station()

        for station in station_list:
            print(station)

        return

    programs = schedule.get_prgrams(station)

    for program in programs:
        print(program)


if __name__ == "__main__":
    main()
