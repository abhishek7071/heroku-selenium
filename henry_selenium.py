from selenium import webdriver
import os
import pandas
#參考 https://www.youtube.com/watch?v=Ven-pqwk3ec


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
#driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)
driver = webdriver.Chrome(r"C:\Users\user\Desktop\聯成助教資料\練習\chromedriver")
url = "https://fuli.gamer.com.tw/shop.php"

driver.get(url)
#selenium-使用 https://jzchangmark.wordpress.com/2015/03/16/selenium-%E4%BD%BF%E7%94%A8-css-locator-%E5%AE%9A%E4%BD%8D%E5%85%83%E4%BB%B6/
titles = driver.find_elements_by_class_name('items-title')
hrefs = driver.find_elements_by_css_selector("a[class=items-card][href^='https']")#找尋tag為a,class為items-card,href的開頭為https
imgs = driver.find_elements_by_css_selector("div.card-left.flex-center > img")
Popularitys = driver.find_elements_by_css_selector("div.card-right div.items-instructions")

listall1 = []
for i in range(len(titles)):
    x,y,z=0+i*3,1+i*3,2+i*3
    
    listall1.append([titles[i].text,hrefs[i].get_attribute('href'),imgs[i].get_attribute('src'),Popularitys[x].text.split('\n')[0],Popularitys[x].text.split('\n')[1],Popularitys[y].text.replace(' ',':',1),Popularitys[z].text.replace('\n',':',1).replace('\n',"")])

print(listall1)

df1 =pandas.DataFrame(listall1,columns=["title","href","img","人氣","商品數量","活動時間","購買方式"])