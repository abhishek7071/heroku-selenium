import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import datetime
import pandas
import time

#參考 https://www.youtube.com/watch?v=Ven-pqwk3ec (讓heroku上可以使用selenium)


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)


def parse_source(url):
    #driver = webdriver.Chrome(r"chromedriver的路徑")#本機測試用
    driver.get(url)
    soup =  BeautifulSoup(driver.page_source)
    hrefs = soup.find_all('a','lnk vLink')
    return parse_detail(hrefs[0]['href'])

def parse_detail(url):
    driver.get(url)
    res = BeautifulSoup(driver.page_source)
    short_url = res.find('meta',property="og:url")['content'].split("-")[-1]
    href = "https://today.line.me/TW/pc/article/{}?utm_source=copyshare".format(short_url)
    title = res.find('meta',property="og:title")['content'].replace('【TODAY 看世界】','').replace('TODAY 看世界 | ','')
    # resq = requests.get('https://today.line.me/tw/article/%E7%A2%BA%E8%A8%BA%E6%95%B8%E9%AB%98%E5%B1%85%E5%85%A8%E7%90%83%E7%AC%AC5+%E6%AD%BB%E4%BA%A1%E7%8E%87%E5%8D%BB%E5%83%851+%E5%BE%B7%E5%9C%8B%E7%9A%84%E4%BD%9C%E6%B3%95%E7%9C%9F%E8%83%BD%E6%9C%89%E6%95%88%E9%98%B2%E7%96%AB%E5%97%8E%EF%BC%9F-1Ego09') #測試用requests的方式是否可以成功
    # res = bs(resq.text)
    time_s = res.find('p','date').text.strip().replace('發布時間 : ','')
    time_s = datetime.datetime.strptime(time_s, '%Y年%m月%d日%H:%M')
    article = res.find('article','video-cont').text.strip().split("《TODAY 看世界》")[0]
    return {"href":href,"title":title,"time":time_s,"article":article}   


from apscheduler.schedulers.blocking import BlockingScheduler
#參考 https://github.com/maloyang/heroku-clock-howto (heroku上設定排程)
#https://codertw.com/%E4%BC%BA%E6%9C%8D%E5%99%A8/169097/

sched = BlockingScheduler()

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=20)
#@sched.scheduled_job('cron',day_of_week='mon-fri', hour=24)#,minute=45
def timed_job():   
    url = 'https://today.line.me/TW/publisher/101508'
    #df4 = pandas.DataFrame(list(parse_source(url)))
    df4 = parse_source(url)
    now = datetime.datetime.now()
    now_s = now.strftime("%Y-%m-%d")
    time_s = str(df4["time"]).split(' ')[0]
    while(True):
        df4 = parse_source(url)
        time_s = str(df4["time"]).split(' ')[0] 
        now = datetime.datetime.now()   
        if now_s == time_s:
            token = 'Line Notify所給的token'
            headers = {
                'Content-type': 'application/x-www-form-urlencoded',
                'Authorization': f'Bearer {token}'
            }
            
            payload = {
             'message':'\n\n{}\n\n{}\n\n{}\n\n{}'.format(df4["title"],df4["time"],df4["href"],df4["article"]),
            }
            
            res = requests.post('https://notify-api.line.me/api/notify', data = payload, headers = headers)
            break
        
        elif now.hour>=21 :
            break
        else:
            time.sleep(60)
            print(now)
            continue
 

sched.add_job(timed_job, 'cron', day_of_week='mon-fri', hour=19,minute = 1)

sched.start()

