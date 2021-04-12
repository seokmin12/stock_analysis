from selenium import webdriver
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# UserAgent값을 바꿔줍시다!
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome(executable_path="/Users/seokmin/Desktop/python/chromedriver", chrome_options=options)
url = 'https://finance.daum.net/domestic/after_hours?market=KOSDAQ'
driver.get(url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')

company_list = []

for n in range(0, 15):
    n += 1
    company = soup.select_one(f"#boxAfterHours > div.box_contents > div:nth-child(1) > table > tbody > tr:nth-child({n}) > td").a['href']
    company = company.replace("/quotes/A", "")
    company_list.append(company)
print(company_list)
driver.quit()
