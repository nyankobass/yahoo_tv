# yahoo_tv
Tools for Acquiring Japanese TV Schedule

# Description
seleniumを使ってYahoo TVにアクセスし、番組表を取得する

# Requirement
* python 3.7.0  
* Chrome 59 以降  
* ChromeDriver

# Install
`$ git clone`した後  
`$ python setup install`

selniumを利用するため、ChromeDriverを適切なディレクトリに保存する。  
http://chromedriver.chromium.org/downloads

# Usage
* ヘルプを表示する  
`$ python -m yahoo_tv --help`

* エリア一覧を表示する  
`$ python -m yahoo_tv --pref-list`

* 放送局一覧を表示する  
`$ python -m yahoo_tv -p 23 --station-list -c [chromedriver.exeへのPATH]`

* 現在から24時間分の番組表を取得する  
`$ python -m yahoo_tv -p 23 -c [chromedriver.exeへのPATH]`

* 指定した放送局の現在から24時間分の番組表を取得する  
`$ python -m yahoo_tv -p 23 -s テレビ東京 -c [chromedriver.exeへのPATH]`

* 指定した日付の番組表を取得する  
`$ python -m yahoo_tv -p 23 -d 2018-10-12 -s テレビ東京 -c [chromedriver.exeへのPATH]`

# Sample Code
```
import sys  
import datetime  
  
import yahoo_tv  
  
chromedriver = "D:\chromedriver.exe"  
  
tv = yahoo_tv.API(chromedriver)  
  
# 東京は23  
pref_code = 23  
  
# 日付を指定  
dt = datetime.datetime.today()  
  
schedule = tv.get_schedule(pref_code, dt)  
  
if schedule is None:  
    print("Error...")  
    sys.exit(1)  
  
station_list = schedule.get_all_station()   
  
for station in station_list:  
    print("@@ " + station)  
    program_list = schedule.get_prgrams(station)  
  
    for program in program_list:  
        print(program.format())  
  
sys.exit(0)  
```