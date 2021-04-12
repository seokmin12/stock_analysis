import requests
from bs4 import BeautifulSoup

# company_code = input("어떤 종목의 변동성을 조사할까요? 종목 코드를 써넣으세요: ")

company_code = '256840'

url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}"
response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
html = response.text
soup = BeautifulSoup(html, 'html.parser')

high_price = soup.select_one("body > table.type2 > tr:nth-child(4) > td:nth-child(5)").get_text()  # 실제로 거래할 때 tr의 nth-child '3'으로 바꿔주기
high_price = int(high_price.replace(",", ""))

low_price = soup.select_one("body > table.type2 > tr:nth-child(4) > td:nth-child(6)").get_text()   # 실제로 거래할 때 tr의 nth-child '3'으로 바꿔주기
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

print(f"종목명: {company_code}, 변동폭: {range}, 시초가: {start_price}, 매수할 금액: {target_price}, 현재가: {now_price}, 수익률: {profit_rate}%")

if now_price >= target_price and profit_rate >= 3:
    print("It's time to buy")
else:
    print("Don't buy")
print("======================================================================================")
