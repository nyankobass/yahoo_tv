# yahoo_tv
Tools for Acquiring Japanese TV Schedule

# Description
seleniumを使ってYahoo TVにアクセスし、番組表を取得する

# Requirement
* python 3.7.0  
* Chrome 59 以降  
* ChromeDriver

# Install
`git clone`した後  
`$ python setup develop`

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
`$ python -m yahoo_tv -p 23 -c "D:\chromedriver.exe`

* 指定した放送局の現在から24時間分の番組表を取得する  
`$ python -m yahoo_tv -p 23 -s テレビ東京 -c "D:\chromedriver.exe`

* 指定した日付の番組表を取得する  
`$ python -m yahoo_tv -p 23 -d 2018-10-12 -s テレビ東京 -c "D:\chromedriver.exe`
