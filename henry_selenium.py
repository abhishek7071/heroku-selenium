from selenium import webdriver
import os
#參考 https://www.youtube.com/watch?v=Ven-pqwk3ec


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options= chrome_options)

driver.get("https://www.104.com.tw/job/5rvmg?jobsource=jolist_b_relevance")
print(driver.page_source)