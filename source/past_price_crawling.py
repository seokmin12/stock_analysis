import requests
from bs4 import BeautifulSoup
import datetime

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

company_code = input("어떤 종목의 가격을 조사할까요? 종목 코드를 써넣으세요: ")

f = open(f'history_data/{company_code}.csv', 'w')
f.write("date" + "," + "price" + "\n")

i = 1

final = []
for i in range(20):
    url = f"https://finance.naver.com/item/sise_day.nhn?code={company_code}&page={i}"
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    lists = soup.find_all("tr")
    isCheckNone = None

    for n in range(1, len(lists) - 1):
        if lists[n].span != isCheckNone:
            day = lists[n].find_all("td", align="center")[0].text
            price = lists[n].find_all("td", class_="num")[0].text
            price = price.replace(",", "")

            result = day + "," + price + '\n'
            final.append(result)
            print(result)
f.writelines(final)
f.close()
