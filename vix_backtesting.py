import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from VIX_project.analysis_tool import correlation_analysis, drawdown_calculation, return_calculation


def merge_data():
    # futures_1 = pd.read_csv('data/VIX_futures1_15.csv').rename(columns={'Close': 'Close1', 'High': 'High1', 'Low': 'Low1'})
    # futures_2 = pd.read_csv('data/VIX_futures2_15.csv').rename(columns={'Close': 'Close2', 'High': 'High2', 'Low': 'Low2'})
    # futures_3 = pd.read_csv('data/VIX_futures3_15.csv').rename(columns={'Close': 'Close3', 'High': 'High3', 'Low': 'Low3'})

    futures_1 = pd.read_csv('data/VIX_futures1_15_long_band.csv').rename(
        columns={'Open': 'Open1', 'Close': 'Close1', 'High': 'High1', 'Low': 'Low1'})

    futures_2 = pd.read_csv('data/VIX_futures2_15_long.csv').rename(
        columns={'Open': 'Open2', 'Close': 'Close2', 'High': 'High2', 'Low': 'Low2'})
    temp_data = pd.merge(futures_1, futures_2, how='inner', on='Dates')
    spread = pd.DataFrame(temp_data['Close2'] - temp_data['Close1'], columns=['Spread'])
    temp_data = pd.concat([temp_data, spread], 1)
    temp_data.to_csv('MultiChart_backtesting_data.csv')
    futures_3 = pd.read_csv('data/VIX_futures2_15_long.csv').rename(
        columns={'Open': 'Open3', 'Close': 'Close3', 'High': 'High3', 'Low': 'Low3'})

    data = pd.merge(futures_1, futures_2, how='inner', on='Dates')
    data = pd.merge(data, futures_3, how='inner', on='Dates')

    return data


class strategy_backtesting(object):
    def __init__(self):
        #self.futures_data = pd.read_csv('realtime_data/hr_backtesting_data.csv')
        self.futures_data = pd.read_csv('data/VIX_daily_backtesting_data.csv')
        self.up2 = self.futures_data['up2']
        self.up1 = self.futures_data['up1']
        self.mean = self.futures_data['mean']
        self.down1 = self.futures_data['down1']
        self.down2 = self.futures_data['down2']
        self.vix_pc = self.futures_data['total_vix_pc']
        self.sp_pc = self.futures_data['total_sp_pc']
        self.sp_price = self.futures_data['sp_price']
        self.vix95 = self.futures_data['vix95']
        self.vix70 = self.futures_data['vix70']
        self.sp95 = self.futures_data['sp95']
        self.sp70 = self.futures_data['sp70']
        # self.settlement_day = ['2018/7/18 ', '2018/8/22 ', '2018/9/19 ', '2018/10/17', '2018/11/21',
        #                       '2018/12/19', '2019/1/16 ', '2019/2/13 ']
        self.settlement_day = ['2012/01/17', '2012/02/14', '2012/03/20', '2012/04/17', '2012/05/15', '2012/06/19',
                               '2012/07/17', '2012/08/21', '2012/09/18', '2012/10/16', '2012/11/20', '2012/12/18',
                               '2013/01/15', '2013/02/12', '2013/03/19', '2013/04/16', '2013/05/21', '2013/06/18',
                               '2013/07/16', '2013/08/20', '2013/09/17', '2013/10/15', '2013/11/19', '2013/12/17',
                               '2014/01/21', '2014/02/18', '2014/03/17', '2014/04/15', '2014/05/20', '2014/06/17',
                               '2014/07/15', '2014/08/19', '2014/09/16', '2014/10/21', '2014/11/19', '2014/12/17',
                               '2015/01/21', '2015/02/18', '2015/03/18', '2015/04/15', '2015/05/20', '2015/06/17',
                               '2015/07/22', '2015/08/19', '2015/09/16', '2015/10/21', '2015/11/18', '2015/12/16',
                               '2016/01/20', '2016/02/17', '2016/03/16', '2016/04/20', '2016/05/18', '2016/06/15',
                               '2016/07/20', '2016/08/17', '2016/09/21', '2016/10/19', '2016/11/16', '2016/12/21',
                               '2017/01/18', '2017/02/15', '2017/03/22', '2017/04/19', '2017/05/17', '2017/06/21',
                               '2017/07/19', '2017/08/16', '2017/09/20', '2017/10/18', '2017/11/15', '2017/12/20',
                               '2018/01/17', '2018/02/14', '2018/03/21', '2018/04/18', '2018/05/16', '2018/06/20',
                               '2018/07/18', '2018/08/22', '2018/09/19', '2018/10/17', '2018/11/21', '2018/12/19',
                               '2019/1/16', '2019/2/13', '2019/3/19', '2019/4/17'
                               ]
        self.spread = 0.07
        self.band_range = 36000
        self.spread1_2 = np.array(self.futures_data['Close2']) - np.array(self.futures_data['Close1'])
        self.spread1_2_stats = {'mean': 0.74, 'std': 1.05, 'skew': -2.01, 'kurt': 9.19}
        # self.band1_2 = {'up2': 1.946, 'up1': 1.34, 'down1': -1.1, 'down2': -2.9}

    def PnL_calculation(self, futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list):
        trading_number = 0
        # futures1

        last_status_1 = 'none'
        last_price_1 = self.futures_data['Close1'].iloc[0]
        accumulative_pl_1 = 0
        accumulative_pl_1_list = []

        # futures2

        last_status_2 = 'none'
        last_price_2 = self.futures_data['Close2'].iloc[0]
        accumulative_pl_2 = 0
        accumulative_pl_2_list = []

        last_amount = 0

        for index in range(len(futures1_holding_list)):
            now_status = futures1_holding_list[index]
            now_amount = futures1_amount_list[index]
            now_price = self.futures_data['Close1'].iloc[index]

            if last_status_1 == 'none':
                if now_status == 'none':
                    # no action
                    accumulative_pl_1 += 0
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'buy':
                    # open
                    trading_number += 1
                    print('buy', self.futures_data['Dates'].iloc[index], index, self.futures_data['Close1'].iloc[index])
                    accumulative_pl_1 += (-self.spread) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'sell':
                    # open
                    trading_number += 1
                    print('sell', self.futures_data['Dates'].iloc[index], index, self.futures_data['Close1'].iloc[index])
                    accumulative_pl_1 += (-self.spread) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

            elif last_status_1 == 'sell':
                if now_status == 'none':
                    # close
                    trading_number += 1
                    accumulative_pl_1 += (last_price_1 - now_price - self.spread) * last_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'buy':
                    trading_number += 2
                    #print('buy', self.futures_data['Dates'].iloc[index], index,
                     #     self.futures_data['Close1'].iloc[index])
                    accumulative_pl_1 += (last_price_1 - now_price - 2 * self.spread) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'sell':
                    accumulative_pl_1 += (last_price_1 - now_price) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

            elif last_status_1 == 'buy':
                if now_status == 'none':
                    trading_number += 1
                    print('sell', self.futures_data['Dates'].iloc[index], index, self.futures_data['Close1'].iloc[index])
                    accumulative_pl_1 += (now_price - last_price_1 - self.spread) * last_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'buy':
                    accumulative_pl_1 += (now_price - last_price_1) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

                elif now_status == 'sell':
                    trading_number += 2
                    #print('sell', self.futures_data['Dates'].iloc[index], index, self.futures_data['Close1'].iloc[index])
                    accumulative_pl_1 += (now_price - last_price_1 - 2 * self.spread) * now_amount
                    accumulative_pl_1_list.append(accumulative_pl_1)

            last_amount = now_amount
            last_price_1 = now_price
            last_status_1 = now_status

        for index in range(len(futures2_holding_list)):
            now_status = futures2_holding_list[index]
            now_amount = futures2_amount_list[index]
            now_price = self.futures_data['Close2'].iloc[index]

            if last_status_2 == 'none':
                if now_status == 'none':
                    # no action
                    accumulative_pl_2 += 0
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'buy':
                    # open
                    trading_number += 1
                    accumulative_pl_2 += (-self.spread) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'sell':
                    # open
                    #print('sell', self.futures_data['Dates'].iloc[index], index,
                          #self.futures_data['Close2'].iloc[index])
                    trading_number += 1
                    accumulative_pl_2 += (-self.spread) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

            elif last_status_2 == 'sell':
                if now_status == 'none':
                    # close
                    #print('none', self.futures_data['Dates'].iloc[index], index,
                          #self.futures_data['Close2'].iloc[index])
                    trading_number += 1
                    accumulative_pl_2 += (last_price_2 - now_price - self.spread) * last_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'buy':
                    trading_number += 2
                    accumulative_pl_2 += (last_price_2 - now_price - 2 * self.spread) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'sell':
                    accumulative_pl_2 += (last_price_2 - now_price) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

            elif last_status_2 == 'buy':
                if now_status == 'none':
                    trading_number += 1
                    accumulative_pl_2 += (now_price - last_price_2 - self.spread) * last_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'buy':
                    accumulative_pl_2 += (now_price - last_price_2) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

                elif now_status == 'sell':
                    trading_number += 2
                    accumulative_pl_2 += (now_price - last_price_2 - 2 * self.spread) * now_amount
                    accumulative_pl_2_list.append(accumulative_pl_2)

            last_amount = now_amount
            last_price_2 = now_price
            last_status_2 = now_status

        print('trading number =', trading_number)
        return np.array(accumulative_pl_1_list), np.array(accumulative_pl_2_list)

# -------------------------------------------------- strategy ---------------------------------------------------------

    def condition1(self):
        # 0 -1 0
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []

        last_status = 'none'

        for i in range(len(self.futures_data)):

            if self.futures_data['Dates'].iloc[i][:10] in self.settlement_day:
                # settlement day
                print(self.futures_data['Dates'].iloc[i][:10])
                futures1_holding_list.append('none')
                futures2_holding_list.append('none')
                futures1_amount_list.append(0)
                futures2_amount_list.append(0)

            else:
                if last_status == 'none':

                    last_status = 'short'
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('sell')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(1)

                elif last_status == 'short':
                    if self.spread1_2[i] <= 0:
                        last_status = 'hedge'

                        futures1_holding_list.append('none')
                        futures2_holding_list.append('none')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(0)

                    else:
                        futures1_holding_list.append('none')
                        futures2_holding_list.append('sell')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(1)

                elif last_status == 'hedge':
                    if self.spread1_2[i] >= 0:
                        last_status = 'short'

                        futures1_holding_list.append('none')
                        futures2_holding_list.append('sell')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(1)

                    else:
                        futures1_holding_list.append('none')
                        futures2_holding_list.append('none')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(0)

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def condition2(self):
        # 0 -1 0
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []

        for i in range(len(self.futures_data)):

            if self.futures_data['Dates'].iloc[i][:10] in self.settlement_day:
                # settlement day
                print(self.futures_data['Dates'].iloc[i][:10])
                futures1_holding_list.append('none')
                futures2_holding_list.append('none')
                futures1_amount_list.append(0)
                futures2_amount_list.append(0)

            else:
                futures1_holding_list.append('none')
                futures2_holding_list.append('sell')
                futures1_amount_list.append(0)
                futures2_amount_list.append(1)

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def back1(self):
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'
        temp_holding_sp_price_list = []

        for i in range(len(self.futures_data)):
            if last_status == 'none':

                if self.sp_pc.iloc[i] >= self.sp95.iloc[i] and self.vix_pc.iloc[i] >= self.vix95.iloc[i] \
                        and self.futures_data['Close1'].iloc[i] >= 15:
                #if self.sp_pc.iloc[i] + self.vix_pc.iloc[i] >= self.sp95.iloc[i] + self.vix95.iloc[i] and self.vix_pc.iloc[i] - self.sp_pc.iloc[i] >= 0:
                #    last_status = 'hold'

                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

                    temp_holding_sp_price_list.append(self.sp_price.iloc[i])

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

            elif last_status == 'hold':

                if (self.sp_price.iloc[i] - min(temp_holding_sp_price_list)) / min(temp_holding_sp_price_list) >= 0.015:
                    last_status = 'none'

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                    temp_holding_sp_price_list = []

                else:

                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

                    temp_holding_sp_price_list.append(self.sp_price.iloc[i])

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def back2(self):
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'
        last_band = 0
        now_band = 0
        temp_holding_sp_price_list = []

        for i in range(len(self.futures_data)):

            if last_status == 'none':
                if self.spread1_2[i] <= self.down1.iloc[i]:
                    last_status = 'buy'

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('buy')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(1)

                    temp_holding_sp_price_list.append(self.sp_price.iloc[i])

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

            elif last_status == 'buy':
                if self.spread1_2[i] >= self.down1.iloc[i]:
                    last_status = 'none'
                    temp_holding_sp_price_list = []

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('buy')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(1)

                    temp_holding_sp_price_list.append(self.sp_price.iloc[i])

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def back2_contango_reverse(self):
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'
        stop_loss = 1
        enter_price = 0

        for i in range(len(self.futures_data)):
            if self.up1.iloc[i] <= self.spread1_2[i] < self.up2.iloc[i]:
                now_band = 1

            elif self.spread1_2[i] >= self.up2.iloc[i]:
                now_band = 2

            else:
                now_band = 0

            if last_status == 'none':
                if now_band == 1:
                    last_status = 'reverse'

                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

            elif last_status == 'reverse':
                if self.spread1_2[i] <= self.mean.iloc[i]:
                    last_status = 'none'

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def back2_back_reverse(self):
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'
        stop_loss = 1
        enter_price = 0

        for i in range(len(self.futures_data)):
            if self.down2.iloc[i] < self.spread1_2[i] <= self.down1.iloc[i]:
                now_band = 1

            elif self.spread1_2[i] <= self.down2.iloc[i]:
                now_band = 2

            else:
                now_band = 0

            if last_status == 'none':
                if now_band == 2:
                    last_status = 'reverse'
                    enter_price = self.futures_data['Close1'].iloc[i]

                    futures1_holding_list.append('sell')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

            elif last_status == 'reverse':
                if self.spread1_2[i] >= 0 or self.futures_data['Close1'].iloc[i] - enter_price <= -1.5:
                    last_status = 'none'
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('sell')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(0)

                    enter_price = self.futures_data['Close1'].iloc[i]

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def spread_contango(self):
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'

        for i in range(len(self.futures_data)):

            if last_status == 'none':
                if self.spread1_2[i] >= self.up1.iloc[i]:
                    last_status = 'sell'

                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('sell')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(1)

                else:
                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

            elif last_status == 'sell':
                if self.spread1_2[i] <= self.mean.iloc[i]:
                    last_status = 'none'

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('sell')
                    futures1_amount_list.append(1)
                    futures2_amount_list.append(1)

            elif last_status == 'sell2':
                if self.spread1_2[i] <= self.mean.iloc[i]:
                    last_status = 'none'

                    futures1_holding_list.append('none')
                    futures2_holding_list.append('none')
                    futures1_amount_list.append(0)
                    futures2_amount_list.append(0)

                else:
                    futures1_holding_list.append('buy')
                    futures2_holding_list.append('sell')
                    futures1_amount_list.append(2)
                    futures2_amount_list.append(2)

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def spread_backwardation(self):
        look_back_parameter = 30
        futures1_holding_list = []
        futures2_holding_list = []
        futures1_amount_list = []
        futures2_amount_list = []
        last_status = 'none'
        last_mean_spy_status = 'down'

        for i in range(len(self.futures_data)):

            if i <= look_back_parameter:
                futures1_holding_list.append('none')
                futures2_holding_list.append('none')
                futures1_amount_list.append(0)
                futures2_amount_list.append(0)

            else:
                mean_spy = np.mean(self.sp_price.iloc[i - look_back_parameter: i + 1])
                min_spy = min(self.sp_price.iloc[i - look_back_parameter: i + 1])

                if last_status == 'none':
                    if self.spread1_2[i] <= self.down1.iloc[i] and ((self.sp_price.iloc[i] >= mean_spy and last_mean_spy_status == 'down') or (self.sp_price.iloc[i] - min_spy) >= 90):
                        last_status = 'buy'

                        futures1_holding_list.append('sell')
                        futures2_holding_list.append('buy')
                        futures1_amount_list.append(1)
                        futures2_amount_list.append(1)

                    elif self.spread1_2[i - 1] <= self.down1.iloc[i - 1] and self.spread1_2[i] > self.down1.iloc[i]:
                        last_status = 'buy'

                        futures1_holding_list.append('sell')
                        futures2_holding_list.append('buy')
                        futures1_amount_list.append(1)
                        futures2_amount_list.append(1)

                    else:
                        futures1_holding_list.append('none')
                        futures2_holding_list.append('none')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(0)

                elif last_status == 'buy':
                    if self.spread1_2[i] >= self.mean.iloc[i] or self.sp_price.iloc[i] == mean_spy:
                        last_status = 'none'

                        futures1_holding_list.append('none')
                        futures2_holding_list.append('none')
                        futures1_amount_list.append(0)
                        futures2_amount_list.append(0)

                    else:
                        futures1_holding_list.append('sell')
                        futures2_holding_list.append('buy')
                        futures1_amount_list.append(1)
                        futures2_amount_list.append(1)

                if self.sp_price.iloc[i] > mean_spy:
                    last_mean_spy_status = 'up'

                else:
                    last_mean_spy_status = 'down'

        return futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list

    def strategy_analysis(self):
        date = np.array(self.futures_data['Dates'])

        futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list = self.back2()
        pl_1, pl_2 = self.PnL_calculation(futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list )

        futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list = self.back2_contango_reverse()
        pl_1_b, pl_2_b = self.PnL_calculation(futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list)

        futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list = self.back2_back_reverse()
        pl_1_c, pl_2_c = self.PnL_calculation(futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list,)

        futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list = self.back1()
        pl_1_d, pl_2_d = self.PnL_calculation(futures1_holding_list, futures2_holding_list, futures1_amount_list, futures2_amount_list)

        total_pl = np.array(pl_1_c) + np.array(pl_2_c) + np.array(pl_1_d) + np.array(pl_2_d)
        total_pl = np.array(pl_1_b) + np.array(pl_2_b) + np.array(pl_1_c) + np.array(pl_2_c)# + np.array(pl_1) + np.array(pl_2)# + np.array(pl_1_c) + np.array(pl_2_c) + np.array(pl_1_d) + np.array(pl_2_d)
        total_pl = np.array(pl_1) + np.array(pl_2)# + np.array(pl_1_b) + np.array(pl_2_b) + np.array(pl_1_c) + np.array(pl_2_c)
        # ---------- daily pnl -----------
        pl_1_daily_list = []
        pl_2_daily_list = []
        pl_1_b_daily_list = []
        pl_2_b_daily_list = []
        pl_1_c_daily_list = []
        pl_2_c_daily_list = []
        pl_1_d_daily_list = []
        pl_2_d_daily_list = []
        date_daily_list = []

        for index in range(len(date) - 1):
            now_date = date[index][:10]
            next_date = date[index + 1][:10]

            if now_date != next_date:
                pl_1_daily_list.append(pl_1[index])
                pl_2_daily_list.append(pl_2[index])
                pl_1_b_daily_list.append(pl_1_b[index])
                pl_2_b_daily_list.append(pl_2_b[index])
                pl_1_c_daily_list.append(pl_1_c[index])
                pl_2_c_daily_list.append(pl_2_c[index])
                pl_1_d_daily_list.append(pl_1_d[index])
                pl_2_d_daily_list.append(pl_2_d[index])
                date_daily_list.append(now_date)

        total_pl_1_daily = np.array(pl_1_daily_list) + np.array(pl_2_daily_list)
        total_pl_b_daily = np.array(pl_1_b_daily_list) + np.array(pl_2_b_daily_list)
        total_pl_c_daily = np.array(pl_1_c_daily_list) + np.array(pl_2_c_daily_list)
        total_pl_d_daily = np.array(pl_1_d_daily_list) + np.array(pl_2_d_daily_list)
        total_pl_daily = total_pl_b_daily + total_pl_1_daily + total_pl_c_daily

        # ----------- diff calculation -----------

        diff_total_pl_1_daily = np.array(pd.DataFrame(total_pl_1_daily).diff().dropna())
        diff_total_pl_1_daily.shape = (1, len(diff_total_pl_1_daily))
        diff_total_pl_1_daily = diff_total_pl_1_daily[0]

        diff_total_pl_b_daily = np.array(pd.DataFrame(total_pl_b_daily).diff().dropna())
        diff_total_pl_b_daily.shape = (1, len(diff_total_pl_b_daily))
        diff_total_pl_b_daily = diff_total_pl_b_daily[0]

        diff_total_pl_daily = diff_total_pl_1_daily + diff_total_pl_b_daily

        # ----------- monthly pnl -------------

        pl_1_monthly_list = []
        pl_2_monthly_list = []
        pl_1_b_monthly_list = []
        pl_2_b_monthly_list = []
        date_monthly_list = []

        for day_index in range(len(date_daily_list) - 1):
            now_date = date_daily_list[day_index][:7]
            next_date = date_daily_list[day_index + 1][:7]

            if now_date != next_date:
                pl_1_monthly_list.append(pl_1_daily_list[day_index])
                pl_2_monthly_list.append(pl_2_daily_list[day_index])
                pl_1_b_monthly_list.append(pl_1_b_daily_list[day_index])
                pl_2_b_monthly_list.append(pl_2_b_daily_list[day_index])
                date_monthly_list.append(now_date)

        total_pl_1_monthly = np.array(pl_1_monthly_list) + np.array(pl_2_monthly_list)
        total_pl_b_monthly = np.array(pl_1_b_monthly_list) + np.array(pl_2_b_monthly_list)
        total_pl_monthly = total_pl_b_monthly + total_pl_1_monthly

        # ----------- year pnl -------------------

        total_pl_year = []

        for month_index in range(len(date_monthly_list) - 1):
            now_date = date_monthly_list[month_index][:4]
            next_date = date_monthly_list[month_index + 1][:4]

            if now_date != next_date:
                total_pl_year.append(total_pl_monthly[month_index])

        # ----------- diff calculation -----------

        diff_total_pl_1_monthly = np.array(pd.DataFrame(total_pl_1_monthly).diff().dropna())
        diff_total_pl_1_monthly.shape = (1, len(diff_total_pl_1_monthly))
        diff_total_pl_1_monthly = diff_total_pl_1_monthly[0]

        diff_total_pl_b_monthly = np.array(pd.DataFrame(total_pl_b_monthly).diff().dropna())
        diff_total_pl_b_monthly.shape = (1, len(diff_total_pl_b_monthly))
        diff_total_pl_b_monthly = diff_total_pl_b_monthly[0]

        diff_total_pl_monthly = diff_total_pl_1_monthly + diff_total_pl_b_monthly

        # ----------- daily maximum profit and loss ---------------
        print(total_pl_year)

        # max profit

        #print('單日最大獲利 ', 'contango:', round(max(diff_total_pl_1_daily), 2),
        #      'backwardation:', round(max(diff_total_pl_b_daily), 2), 'total:', round(max(diff_total_pl_daily), 2))
        #print('單月最大獲利 ', 'contango:', round(max(diff_total_pl_1_monthly), 2),
        #      'backwardation:', round(max(diff_total_pl_b_monthly), 2), 'total:', round(max(diff_total_pl_monthly), 2))
#
        ## max loss
#
        #print('單日最大損失 ', 'contango:', round(min(diff_total_pl_1_daily), 2),
        #      'backwardation:', round(min(diff_total_pl_b_daily), 2), 'total:', round(min(diff_total_pl_daily), 2))
        #print('單月最大損失 ', 'contango:', round(min(diff_total_pl_1_monthly), 2),
        #      'backwardation:', round(min(diff_total_pl_b_monthly), 2), 'total:', round(min(diff_total_pl_monthly), 2))
#
        ## --------- percentile --------
        #print('contango 25分位數 ', round(np.percentile(diff_total_pl_1_daily, [25])[0], 2),
        #      'contango 中位數 ', round(np.percentile(diff_total_pl_1_daily, [50])[0], 2),
        #      'contango 75分位數 ', round(np.percentile(diff_total_pl_1_daily, [75])[0], 2))
#
        #print('backwardation 25分位數 ', round(np.percentile(diff_total_pl_b_daily, [25])[0], 2),
        #      'backwardation 中位數 ', round(np.percentile(diff_total_pl_b_daily, [50])[0], 2),
        #      'backwardation 75分位數 ', round(np.percentile(diff_total_pl_b_daily, [75])[0], 2))
#
        #print('total 25分位數 ', round(np.percentile(diff_total_pl_daily, [25])[0], 2),
        #      'total 中位數 ', round(np.percentile(diff_total_pl_daily, [50])[0], 2),
        #      'total 75分位數 ', round(np.percentile(diff_total_pl_daily, [75])[0], 2))
#
        #print('monthly contango 25分位數 ', round(np.percentile(diff_total_pl_1_monthly, [25])[0], 2),
        #      'monthly contango 中位數 ', round(np.percentile(diff_total_pl_1_monthly, [50])[0], 2),
        #      'monthly contango 75分位數 ', round(np.percentile(diff_total_pl_1_monthly, [75])[0], 2))
#
        #print('monthly backwardation 25分位數 ', round(np.percentile(diff_total_pl_b_monthly, [25])[0], 2),
        #      'monthly backwardation 中位數 ', round(np.percentile(diff_total_pl_b_monthly, [50])[0], 2),
        #      'monthly backwardation 75分位數 ', round(np.percentile(diff_total_pl_b_monthly, [75])[0], 2))
#
        #print('monthly total 25分位數 ', round(np.percentile(diff_total_pl_monthly, [25])[0], 2),
        #      'monthly total 中位數 ', round(np.percentile(diff_total_pl_monthly, [50])[0], 2),
        #      'monthly total 75分位數 ', round(np.percentile(diff_total_pl_monthly, [75])[0], 2))
#
        ## ---------- return MDD holding period and stagnation ---------
        #print('backwardation 持倉時間 ', len(np.where(diff_total_pl_b_daily != 0)[0]))
#
        print('return ', return_calculation(total_pl_daily), 'MDD ', drawdown_calculation(total_pl_daily)[0],
              'ratio ', round(return_calculation(total_pl_daily) / drawdown_calculation(total_pl_daily)[0], 2),
              'index ', drawdown_calculation(total_pl_daily)[1], 'stagnation ', drawdown_calculation(total_pl_daily)[2])

        # ---------- plot ----------

        plt.subplot(2, 1, 1)
        plt.plot(total_pl)
        plt.legend(['PnL'])
        plt.axvline(drawdown_calculation(total_pl)[1], linestyle='--', color='r')
        # plt.axvline(4087, linestyle='-', color='g')
        # plt.axvline(12544, linestyle='-', color='g')
        # plt.axvline(25560, linestyle='-', color='g')
        # plt.axvline(42502, linestyle='-', color='g')
        # plt.axvline(62124, linestyle='-', color='g')
        # plt.axvline(80785, linestyle='-', color='g')
        # plt.axvline(101224, linestyle='-', color='g')

        plt.subplot(2, 1, 2)
        plt.plot(np.array(self.futures_data['Close2']) - np.array(self.futures_data['Close1']), 'g')
        plt.legend(['spread1_2'], loc='upper right')
        plt.twinx()
        plt.plot(np.array(self.futures_data['Close1']), 'r')
        plt.legend(['front'], loc='upper left')
        # plt.axhline(22)
        plt.plot()
        plt.show()

    def plot(self):
        plt.plot(self.spread1_2)
        plt.plot(self.up1)
        plt.plot(self.up2)
        plt.plot(self.mean)
        plt.plot(self.down1)
        plt.plot(self.down2)

        plt.show()


if __name__ == '__main__':
    strategy_backtesting = strategy_backtesting()
    strategy_backtesting.strategy_analysis()
