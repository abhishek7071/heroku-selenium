import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import datetime
import pandas


#參考 https://www.youtube.com/watch?v=Ven-pqwk3ec (讓heroku上可以使用selenium)


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)

def parse_source(url):
    #driver = webdriver.Chrome(r"C:\Users\user\Desktop\聯成助教資料\練習\chromedriver")
    driver.get(url)
    soup =  BeautifulSoup(driver.page_source)
    hrefs = soup.find_all('a','lnk vLink')
    for href in hrefs:
        #print(href['href'],'\n')
        yield parse_detail(href['href'])
def parse_detail(url):
    driver.get(url)
    res = BeautifulSoup(driver.page_source)
    short_url = res.find('meta',property="og:url")['content'].split("-")[-1]
    href = "https://today.line.me/TW/pc/article/{}?utm_source=copyshare".format(short_url)
    title = res.find('meta',property="og:title")['content'].replace('【TODAY 看世界】','').replace('TODAY 看世界 | ','')
    # resq = requests.get('https://today.line.me/tw/article/%E7%A2%BA%E8%A8%BA%E6%95%B8%E9%AB%98%E5%B1%85%E5%85%A8%E7%90%83%E7%AC%AC5+%E6%AD%BB%E4%BA%A1%E7%8E%87%E5%8D%BB%E5%83%851+%E5%BE%B7%E5%9C%8B%E7%9A%84%E4%BD%9C%E6%B3%95%E7%9C%9F%E8%83%BD%E6%9C%89%E6%95%88%E9%98%B2%E7%96%AB%E5%97%8E%EF%BC%9F-1Ego09') #測試用requests的方式是否可以成功
    # res = bs(resq.text)
    time = res.find('dd','date').text.replace('發布時間 ','')
    time = datetime.datetime.strptime(time, '%Y年%m月%d日%H:%M')
    text1 = res.find('article','bx-dsc').text.strip()+'\n'+res.find('article','bx-dsc').find_all('p')[1].text.replace(u'\u3000',u'')
    article = text1.split("《TODAY 看世界》")[0]
    return {"href":href,"title":title,"time":time,"article":article}   

#driver = webdriver.Chrome(r"C:\Users\user\Desktop\聯成助教資料\練習\chromedriver")

from apscheduler.schedulers.blocking import BlockingScheduler
#參考 https://github.com/maloyang/heroku-clock-howto (heroku上設定排程)
sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():   
    url = 'https://today.line.me/TW/publisher/101508'
    df4 = pandas.DataFrame(list(parse_source(url)))
    token = 'kEujm1BoMS0AvgNnF8QQ8RHXbUgO3viRsI3oFrZNhTT'
    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
        'Authorization': f'Bearer {token}'
    }
    
    payload = {
     'message':'\n\n{}\n\n{}\n\n{}\n\n{}'.format(df4.iloc[0]["title"],df4.iloc[0]["time"],df4.iloc[0]["href"],df4.iloc[0]["article"]),
    }
    
    res = requests.post('https://notify-api.line.me/api/notify', data = payload, headers = headers)

sched.start()


#driver = webdriver.Chrome(r"C:\Users\user\Desktop\聯成助教資料\練習\chromedriver")
# url = "https://fuli.gamer.com.tw/shop.php"

# driver.get(url)
# #selenium-使用 https://jzchangmark.wordpress.com/2015/03/16/selenium-%E4%BD%BF%E7%94%A8-css-locator-%E5%AE%9A%E4%BD%8D%E5%85%83%E4%BB%B6/
# titles = driver.find_elements_by_class_name('items-title')
# hrefs = driver.find_elements_by_css_selector("a[class=items-card][href^='https']")#找尋tag為a,class為items-card,href的開頭為https
# imgs = driver.find_elements_by_css_selector("div.card-left.flex-center > img")
# Popularitys = driver.find_elements_by_css_selector("div.card-right div.items-instructions")

# listall1 = []
# for i in range(len(titles)):
#     x,y,z=0+i*3,1+i*3,2+i*3
    
#     listall1.append([titles[i].text,hrefs[i].get_attribute('href'),imgs[i].get_attribute('src'),Popularitys[x].text.split('\n')[0],Popularitys[x].text.split('\n')[1],Popularitys[y].text.replace(' ',':',1),Popularitys[z].text.replace('\n',':',1).replace('\n',"")])

# print(listall1)

# df1 =pandas.DataFrame(listall1,columns=["title","href","img","人氣","商品數量","活動時間","購買方式"])