import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':

    settlement_day = ['2017/8/16', '2017/9/20', '2017/10/18', '2017/11/15', '2017/12/20',
                      '2018/1/17', '2018/2/14', '2018/3/21', '2018/4/18', '2018/5/16', '2018/6/20',
                      '2018/7/18', '2018/8/22', '2018/9/19', '2018/10/17', '2018/11/21', '2018/12/19',
                      '2019/1/16', '2019/2/13', '2019/3/19', '2019/4/17', '2019/5/22', '2019/6/19', '2019/7/17',
                      '2019/8/21', '2019/9/18']

    data = pd.read_excel('data/uxfvs.xlsx')
    ux_date = data['UX_Dates']
    ux1_price = data['UX1_LAST']
    ux2_price = data['UX2_LAST']
    arbitrage_index_before = []
    arbitrage_index_after = []

    for settlement in settlement_day:
        temp_index = np.where(ux_date == settlement)[0][0]
        for j in range(temp_index - 4, temp_index + 1):
            arbitrage_index_before.append(j)

        for k in range(temp_index + 1, temp_index + 5):
            arbitrage_index_after.append(k)

    # major strategy
    major_short_pnl_list = []
    major_short_pnl = 0
    major_long_pnl_list = []
    major_long_pnl = 0

    arbitrage1_short_pnl_list = []
    arbitrage1_short_pnl = 0
    arbitrage1_long_pnl_list = []
    arbitrage1_long_pnl = 0

    for i in range(len(ux_date) - 1):
        if i in arbitrage_index_before:
            temp_short_pnl = ux1_price.iloc[i] - ux1_price.iloc[i + 1]
            temp_long_pnl = ux2_price.iloc[i + 1] - ux2_price.iloc[i]

            arbitrage1_long_pnl += temp_long_pnl
            arbitrage1_short_pnl += temp_short_pnl
            arbitrage1_long_pnl_list.append(major_long_pnl)
            arbitrage1_short_pnl_list.append(major_short_pnl)

        elif i in arbitrage_index_after:
            temp_short_pnl = ux2_price.iloc[i] - ux2_price.iloc[i + 1]
            temp_long_pnl = ux1_price.iloc[i + 1] - ux1_price.iloc[i]

            arbitrage1_long_pnl += temp_long_pnl
            arbitrage1_short_pnl += temp_short_pnl
            arbitrage1_long_pnl_list.append(major_long_pnl)
            arbitrage1_short_pnl_list.append(major_short_pnl)

        else:
            temp_short_pnl = ux1_price.iloc[i] - ux1_price.iloc[i + 1]
            temp_long_pnl = ux2_price.iloc[i + 1] - ux2_price.iloc[i]
            major_long_pnl += temp_long_pnl
            major_short_pnl += temp_short_pnl
            major_long_pnl_list.append(major_long_pnl)
            major_short_pnl_list.append(major_short_pnl)

    #plt.plot(np.array(major_short_pnl_list) + np.array(major_long_pnl_list), 'r')
    # plt.plot(arbitrage1_long_pnl_list, 'r')
    # plt.plot(arbitrage1_short_pnl_list)
    plt.plot(np.array(arbitrage1_short_pnl_list) + np.array(arbitrage1_long_pnl_list))
    plt.show()
