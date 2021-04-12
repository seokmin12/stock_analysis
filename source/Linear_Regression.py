import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

f = pd.read_csv("history_data/021320.csv")
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

print('a:', a, 'b:', b)

# 그래프를 그리기 위해 회귀선의 x, y 데이터를 구합니다.
line_x = np.arange(min(x_data), max(x_data), 0.01)
line_y = a * line_x + b

# 붉은색 실선으로 회귀선을 그립니다.
plt.plot(line_x, line_y, 'r-')

plt.plot(x_data, y_data)
plt.title('Stock Price Predict')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(['Predict', 'Real'])

plt.show()

# plt.plot(x_data, y_data)
# plt.xlabel("Date")
# plt.ylabel("Price")
# plt.show()
