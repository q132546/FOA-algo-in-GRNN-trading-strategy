import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    vix_index = pd.read_csv('data/VIX_index.csv')
    futures_price = pd.read_csv('data/VX1VX2_daily.csv')
    sp_price = pd.read_csv('data/sp500.csv')
    data = pd.merge(vix_index, sp_price, on='Dates')
    data = pd.merge(data, futures_price, on='Dates')
    data.to_csv('data/time_value_research.csv', index=False)
    exit()

    settlement_day = ['2014/1/21', '2014/2/18', '2014/3/17', '2014/4/15', '2014/5/20', '2014/6/17',
                      '2014/7/15', '2014/8/19', '2014/9/16', '2014/10/21', '2014/11/19', '2014/12/17',
                      '2015/1/21', '2015/2/18', '2015/3/18', '2015/4/15', '2015/5/20', '2015/6/17',
                      '2015/7/22', '2015/8/19', '2015/9/16', '2015/10/21', '2015/11/18', '2015/12/16',
                      '2016/1/20', '2016/2/17', '2016/3/16', '2016/4/20', '2016/5/18', '2016/6/15',
                      '2016/7/20', '2016/8/17', '2016/9/21', '2016/10/19', '2016/11/16', '2016/12/21',
                      '2017/1/18', '2017/2/15', '2017/3/22', '2017/4/19', '2017/5/17', '2017/6/21',
                      '2017/7/19', '2017/8/16', '2017/9/20', '2017/10/18', '2017/11/15', '2017/12/20',
                      '2018/1/17', '2018/2/14', '2018/3/21', '2018/4/18', '2018/5/16', '2018/6/20',
                      '2018/7/18', '2018/8/22', '2018/9/19', '2018/10/17', '2018/11/21', '2018/12/19',
                      '2019/1/16', '2019/2/13', '2019/3/19']

    dates = np.array(data['Dates'])
    settlement_index_list = []

    for i in range(len(settlement_day)):
        index = np.where(dates == settlement_day[i])[0][0]
        settlement_index_list.append(index)

        #plt.subplot(2, 1, 1)
        #plt.plot(data['VIX'][1000:], color='b')
        #plt.axvline(index, linestyle='--', color='r')

        #plt.subplot(2, 1, 2)
        #plt.plot(data['SP_LAST'][1000:], color='b')
        #plt.axvline(index, linestyle='--', color='r')
    for i in range(len(settlement_index_list) - 1):
        start = settlement_index_list[i] + 1
        end = settlement_index_list[i + 1]
        vix1 = np.array(data['UX1_LAST'].iloc[start:end])
        vix2 = np.array(data['UX2_LAST'].iloc[start:end])
        sp_price = np.array(data['SP_LAST'].iloc[start:end])

        if vix2[0] >= 18:
            pass

        else:
            plt.subplot(3, 1, 1)
            #price = price - price[0]
            plt.plot(vix1)
            plt.plot(vix2, 'r')
            plt.subplot(3, 1, 2)
            plt.plot(vix2 - vix1)
            plt.subplot(3, 1, 3)
            plt.plot(sp_price)

            plt.show()


