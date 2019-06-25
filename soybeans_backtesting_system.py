import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt


class backtesting_framework():
    def __init__(self):
        self.data = pd.read_csv('soybeans_data/soybeans_backtesting_data.csv')
        self.net_position = pd.read_csv('soybeans_data/net_position.csv')

    def main(self):
        print(self.data)
        print(self.net_position)


if __name__ == '__main__':
    backtesting_framework = backtesting_framework()
    backtesting_framework.main()
