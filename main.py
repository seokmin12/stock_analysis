from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#############################################################################################################
#############################################################################################################
# 종목 찾기
#############################################################################################################
#############################################################################################################

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

# UserAgent값을 바꿔줍시다!
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

driver = webdriver.Chrome(executable_path="/Users/seokmin/Desktop/python/chromedriver", chrome_options=options)
url = 'https://finance.daum.net/domestic/after_hours?market=KOSDAQ'
driver.get(url)
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')

company_list = []

for n in range(0, 15):
    n += 1
    company = \
        soup.select_one(
            f"#boxAfterHours > div.box_contents > div:nth-child(1) > table > tbody > tr:nth-child({n}) > td").a[
            'href']
    company = company.replace("/quotes/A", "")
    company_list.append(company)
driver.quit()


#############################################################################################################
#############################################################################################################
# 과거 데이터 모으기
#############################################################################################################
#############################################################################################################

def get_past_day(company_code):
    final_day = []
    for i in range(20):
        get_past_price_url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}&page={i}"
        get_past_price_response = requests.get(get_past_price_url, headers={'User-agent': 'Mozilla/5.0'})
        html = get_past_price_response.text
        get_past_price_soup = BeautifulSoup(html, 'html.parser')

        lists = get_past_price_soup.find_all("tr")
        isCheckNone = None

        for n in range(1, len(lists) - 1):
            if lists[n].span != isCheckNone:
                day = lists[n].find_all("td", align="center")[0].text
                final_day.append(day)
    return final_day


def get_past_price(company_code):
    final_price = []
    for i in range(20):
        get_past_price_url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}&page={i}"
        get_past_price_response = requests.get(get_past_price_url, headers={'User-agent': 'Mozilla/5.0'})
        html = get_past_price_response.text
        get_past_price_soup = BeautifulSoup(html, 'html.parser')

        lists = get_past_price_soup.find_all("tr")
        isCheckNone = None

        for n in range(1, len(lists) - 1):
            if lists[n].span != isCheckNone:
                # day = lists[n].find_all("td", align="center")[0].text
                price = lists[n].find_all("td", class_="num")[0].text
                price = price.replace(",", "")

                final_price.append(price)
    return final_price


def collect_past_data(company_code):
    f = open(f'history_data/{company_code}.csv', 'w')
    f.write("date" + "," + "price" + "\n")
    final = []
    for i in range(20):
        get_past_price_url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}&page={i}"
        get_past_price_response = requests.get(get_past_price_url, headers={'User-agent': 'Mozilla/5.0'})
        html = get_past_price_response.text
        get_past_price_soup = BeautifulSoup(html, 'html.parser')

        lists = get_past_price_soup.find_all("tr")
        isCheckNone = None

        for n in range(1, len(lists) - 1):
            if lists[n].span != isCheckNone:
                day = lists[n].find_all("td", align="center")[0].text
                price = lists[n].find_all("td", class_="num")[0].text
                price = price.replace(",", "")

                result = day + "," + price + '\n'
                final.append(result)
    f.writelines(final)
    f.close()
    return final


def get_strategy(company_code):
    strategy_url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}"
    strategy_response = requests.get(strategy_url, headers={'User-agent': 'Mozilla/5.0'})
    strategy_html = strategy_response.text
    strategy_soup = BeautifulSoup(strategy_html, 'html.parser')

    high_price = strategy_soup.select_one(
        "body > table.type2 > tr:nth-child(4) > td:nth-child(5)").get_text()  # 실제로 거래할 때 tr의 nth-child '3'으로 바꿔주기
    high_price = int(high_price.replace(",", ""))

    low_price = strategy_soup.select_one(
        "body > table.type2 > tr:nth-child(4) > td:nth-child(6)").get_text()  # 실제로 거래할 때 tr의 nth-child '3'으로 바꿔주기
    low_price = int(low_price.replace(",", ""))

    range = high_price - low_price
    strategy = range * 0.5

    now_price_url = "https://finance.naver.com/item/main.nhn?code=" + company_code
    now_price_response = requests.get(now_price_url)
    now_price_html = now_price_response.text
    now_price_soup = BeautifulSoup(now_price_html, 'html.parser')

    now_price_location = now_price_soup.find("p", class_="no_today")
    now_price = now_price_location.select_one("span.blind").get_text()
    now_price = int(now_price.replace(",", ""))

    start_price_location = now_price_soup.find("td", class_="first")
    start_price = start_price_location.select_one("span.blind").get_text()
    start_price = int(start_price.replace(",", ""))

    target_price = start_price + strategy

    profit_rate = (now_price / target_price - 1) * 100 - 0.288
    profit_rate = round(profit_rate, 2)

    print(
        f"종목명: {company_code}, 변동폭: {range}, 시초가: {start_price}, 매수할 금액: {target_price}, 현재가: {now_price}, 수익률: {profit_rate}%")

    if now_price >= target_price and profit_rate >= 3:
        print("It's time to buy")
    else:
        print("Don't buy")


num = -1

company_codes = company_list
fig, axes = plt.subplots(3, 5, figsize=(16, 16))
ax = axes.flatten()

for item in company_codes:
    collect_past_data(item)
    get_past_day(item)
    get_past_price(item)

    #############################################################################################################
    #############################################################################################################
    # 과거 데이터로 추세선 그리기
    #############################################################################################################
    #############################################################################################################

    f = pd.read_csv(f"history_data/{item}.csv")
    date_data = f["date"].sort_index(ascending=False).values.tolist()
    price_data = f["price"].sort_index(ascending=False).values.tolist()

    x_data = list(range(6000, 6000 + 10 * len(date_data), 10))
    y_data = price_data

    # X, Y의 평균을 구합니다.
    x_bar = sum(x_data) / len(x_data)
    y_bar = sum(y_data) / len(y_data)

    # 최소제곱법으로 a, b를 구합니다.
    a = sum([(y - y_bar) * (x - x_bar) for y, x in list(zip(y_data, x_data))])
    a /= sum([(x - x_bar) ** 2 for x in x_data])
    b = y_bar - a * x_bar

    print(f"종목 코드 '{item}'의 데이터를 저장했습니다.")
    get_strategy(item)
    print("======================================================================================")

    # 그래프를 그리기 위해 회귀선의 x, y 데이터를 구합니다.
    line_x = np.arange(min(x_data), max(x_data), 0.01)
    line_y = a * line_x + b

    num += 1

    # 붉은색 실선으로 회귀선을 그립니다.
    ax[num].plot(line_x, line_y, 'r-')

    ax[num].plot(x_data, y_data)
    ax[num].set_title(f'{item}')
    ax[num].legend(['Predict', 'Real'])
plt.tight_layout()
plt.show()
