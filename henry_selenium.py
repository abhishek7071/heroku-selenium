from bs4 import BeautifulSoup
from selenium import webdriver
import os
import datetime
import pandas
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)
    
#browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
print('browser is ready')
url = 'https://mars.nasa.gov/news/'
browser.get(url)
time.sleep(3)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
news_title = soup.find('ul', class_='item_list ').find('li', class_='slide').find('div', class_='content_title')\
    .find('a').get_text()
news_p = soup.find('ul', class_='item_list ').find('li', class_='slide')\
    .find('div', class_='article_teaser_body').get_text()
print(news_title)
