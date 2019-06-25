import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


class backtesting_framework():
    def __init__(self):
        self.data = pd.read_csv('soybeans_backtesting_data.csv')
        self.net_position = pd.read_csv('net_position.csv')
        self.date = np.array(self.data['Dates'])
        self.close = np.array(self.data['S_Close'])
        self.open = np.array(self.data['S_Open'])
        self.upper = np.array(self.data['upper'])
        self.lower = np.array(self.data['lower'])

    def strategy1(self):
        market_position = 0
        last_location = 0
        price_list = []
        temp_price_list = []

        for i in range(len(self.date)):
            #print(self.close[i], self.upper[i], self.lower[i])

            if self.close[i] >= self.upper[i]:
                location = 1

            elif self.close[i] <= self.lower[i]:
                location = -1

            else:
                location = 0

            if market_position == 0 and last_location == 1 and location == 0:
                market_position = 1
                temp_price_list.append(self.close[i])

            elif market_position == 1 and last_location == 0 and location != 0:
                market_position = 0
                temp_price_list.append(self.close[i])
                price_list.append(temp_price_list)

                temp_price_list = []

            elif market_position == 1 and last_location == 0 and location == 0:
                    temp_price_list.append(self.close[i])

            last_location = location

        pl_list = []
        total_pl = 0

        for number in range(len(price_list)):
            last_price = price_list[number][0]
            print(price_list[number])

            for index in range(len(price_list[number])):
                total_pl += last_price - price_list[number][index]
                pl_list.append(total_pl)

                last_price = price_list[number][index]

        plt.plot(self.close)
        plt.plot(self.upper)
        plt.plot(self.lower)
        plt.show()







if __name__ == '__main__':
    backtesting_framework = backtesting_framework()
    backtesting_framework.strategy1()
