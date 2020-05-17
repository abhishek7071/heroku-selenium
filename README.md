##基本說明

-這是一個利用line notify每周1-5自動推播linetoday看世界的機器人

-使用 heroku/selenium/line notify

<img src="https://github.com/henry8082/heroku-selenium/blob/master/S__63660101.jpg" width = "30%" /> <img src="https://github.com/henry8082/heroku-selenium/blob/master/S__63660102.jpg" width = "30%" /> <img src="https://github.com/henry8082/heroku-selenium/blob/master/S__63660099.jpg" width = "30%" />
---------------------------------------
重要設定：

在讓heroku上面能使用要在檔案內另外設定下列參數(<a href="https://www.youtube.com/watch?v=Ven-pqwk3ec">參考網址</a>)

chrome_options = webdriver.ChromeOptions()

chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

chrome_options.add_argument("--headless")

chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)

---------------------------------------
另外在heroku上的Config Vars也要設定下列設置

CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver

GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome


heroku上才能正常使用selenium
---------------------------------------
因推播時間為臺灣時區，跟heroku的時區不同

因此要另外在Config Vars設定下列設置

TZ = Asia/Taipei

---------------------------------------
最後利用apscheduler設定排程(<a href="https://github.com/maloyang/heroku-clock-howto">heroku上設定排程的參考網址</a>)

在henry_selenium.py中設定

sched.add_job(timed_job, 'cron', day_of_week='mon-fri', hour=19,minute = 1)
***
在Procfile中設定clock: python henry_selenium.py

讓heroku能在上面設定的時間開始爬蟲
