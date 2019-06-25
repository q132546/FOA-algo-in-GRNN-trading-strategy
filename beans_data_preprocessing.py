import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn import linear_model, cluster, svm


def Bloomberg_date_transformation():
    data = pd.read_csv('released_data.csv')
    release_date = data['Released Dates']

    new_released_date = []

    for i in range(len(release_date)):
        date = str(release_date.iloc[i])
        # year
        year = date[:4]

        # month
        month = int(date[4:6])

        # day
        day = int(date[6:])

        new_released_date.append(year + '/' + str(month) + '/' + str(day))

    return new_released_date


def delayed_data_modification():
    released_date = pd.read_csv('released_data.csv')
    sup_use_data = pd.read_csv('soybeans_sup$use.csv')
    for i in range(len(released_date)):
        print(released_date['Released Dates'].iloc[i], released_date['Dates'].iloc[i])


def data_merge(training_index):
    s_p_data = pd.read_csv('soybeans_sup$use.csv')
    price_data = pd.read_csv('S1C1.csv')
    ending_quartly_data = pd.read_csv('S_ending_stock&quarterly_position.csv')
    fundamental_data = pd.merge(s_p_data, ending_quartly_data, on='Dates')
    merge_data = pd.merge(price_data, fundamental_data, on='Dates')

    return merge_data.iloc[:training_index], merge_data[training_index:]


def price_range(now_ending_stock, now_sup, selected_number, training_index):
    merge_data_training, merge_data_testing = data_merge(training_index)
    price_ending_stock = int(-288.96 * np.log(0.000137 * np.array(now_ending_stock).astype(np.float)) + 251)

    sup_list = []
    sup_price_dict = {}

    for i in range(len(merge_data_training)):
        sup = merge_data_training['S_Sup'].iloc[i]
        price = merge_data_training['S_Close'].iloc[i]

        if sup not in sup_list:
            sup_list.append(sup)
            sup_price_dict[str(sup)] = []
            sup_price_dict[str(sup)].append(price)

        else:
            sup_price_dict[str(sup)].append(price)

    # sort
    sorted_list = []
    combined_price = []
    diff_list = np.array(sup_list) - now_sup
    positive_list = diff_list[np.where(diff_list >= 0)[0]]
    negative_list = diff_list[np.where(diff_list < 0)[0]]

    if len(positive_list) < selected_number:
        position_length = len(positive_list)

        if position_length != 0:
            for position_index in range(position_length):
                sorted_list.append(positive_list[position_index] + now_sup)

            for position_index in range(selected_number + (selected_number - position_length)):
                sorted_list.append(sorted(negative_list)[-(position_index + 1)] + now_sup)

        else:
            for position_index in range(2 * selected_number):
                sorted_list.append(sorted(negative_list)[-(position_index + 1)] + now_sup)

    elif len(negative_list) < selected_number:
        position_length = len(negative_list)

        if position_length != 0:
            for position_index in range(position_length):
                sorted_list.append(negative_list[position_index] + now_sup)

            for position_index in range(selected_number + (selected_number - position_length)):
                sorted_list.append(sorted(positive_list)[position_index] + now_sup)

        else:
            for position_index in range(2 * selected_number):
                sorted_list.append(sorted(positive_list)[position_index] + now_sup)

    else:

        for sort_index in range(selected_number):
            sorted_list.append(sorted(positive_list)[sort_index] + now_sup)
            sorted_list.append(sorted(negative_list)[-(sort_index + 1)] + now_sup)

    # ---------------------------------------------------------------------------
    temp_mean_list = []
    extreme_count_max = 0
    extreme_count_min = 0

    for i in range(len(sorted_list)):
        # print(sorted_list[i])
        temp_list = sup_price_dict[str(sorted_list[i])]

        if price_ending_stock in range(int(min(temp_list)), int(max(temp_list))):
            combined_price += temp_list

        temp_mean_list.append(np.mean(temp_list))

    if len(combined_price) != 0:
        upper_price = np.mean(combined_price) + np.std(combined_price)
        lower_price = np.mean(combined_price) - np.std(combined_price)

    else:
        positive_mean_price_ending_stock_list = []
        negative_mean_price_ending_stock_list = []

        for temp_mean_list_index, temp_mean in enumerate(temp_mean_list):
            if temp_mean >= price_ending_stock:
                positive_mean_price_ending_stock_list.append(temp_mean_list_index)

            else:
                negative_mean_price_ending_stock_list.append(temp_mean_list_index)

        if len(positive_mean_price_ending_stock_list) > len(negative_mean_price_ending_stock_list):

            for j in positive_mean_price_ending_stock_list:
                combined_price += sup_price_dict[str(sorted_list[j])]

            upper_price = np.mean(combined_price) + np.std(combined_price)
            lower_price = np.mean(combined_price) - np.std(combined_price)

        elif len(positive_mean_price_ending_stock_list) < len(negative_mean_price_ending_stock_list):
            for j in negative_mean_price_ending_stock_list:
                combined_price += sup_price_dict[str(sorted_list[j])]

            upper_price = np.mean(combined_price) + np.std(combined_price)
            lower_price = np.mean(combined_price) - np.std(combined_price)

        else:
            upper_price = price_ending_stock + 50
            lower_price = price_ending_stock - 50

    return upper_price, lower_price

    #
    #for temp_mean_list_index in range(selected_number * 2):
    #    if max(temp_mean_list) - temp_mean_list[temp_mean_list_index] >= 150:
    #        extreme_count_max += 1
    #    elif temp_mean_list[temp_mean_list_index] - min(temp_mean_list) >= 150:
    #        extreme_count_min += 1
#
    #if extreme_count_max == 3:
    #    remove_index = temp_mean_list.index(max(temp_mean_list))
    #    sorted_list.remove(sorted_list[remove_index])
#
    #elif extreme_count_min == 3:
    #    remove_index = temp_mean_list.index(min(temp_mean_list))
    #    sorted_list.remove(sorted_list[remove_index])
#
    ## ------------------------------------------------------------------
#
    #for i in range(len(sorted_list)):
    #    # print(sorted_list[i])
    #    temp_list = sup_price_dict[str(sorted_list[i])]
    #    #print(temp_list)
    #    combined_price += temp_list
    #    #print(np.mean(temp_list), np.std(temp_list), np.percentile(temp_list, 50))
#
    ## combined prob computation
    #sup_mean,  sup_std = np.mean(combined_price), np.std(combined_price)
    #price_ending_stock = -288.96 * np.log(0.000137 * np.array(now_ending_stock).astype(np.float)) + 251
    ##print(price_ending_stock)
    ## print(sup_mean, price_ending_stock)
#
    #upper_price = sup_mean + sup_std
    #lower_price = sup_mean - sup_std
#
    #if price_ending_stock > upper_price:
    #    diff_std = (price_ending_stock - sup_mean) // sup_std
#
    #    upper_price = sup_mean + diff_std * sup_std
    #    lower_price = sup_mean - (1 / diff_std) * sup_std
#
    #elif price_ending_stock < lower_price:
    #    diff_std = (-price_ending_stock + sup_mean) // sup_std
#
    #    upper_price = sup_mean + (1 / diff_std) * sup_std
    #    lower_price = sup_mean - diff_std * sup_std
#
    #else:
    #    pass
#
    #return upper_price, lower_price


def prediction():
    merge_data_training, merge_test = data_merge(2500)
    #for i in range(len(merge_data_training)):
     #   print(merge_data_training['Dates'].iloc[i], merge_data_training['S1_LAST'].iloc[i])

    upper_list = []
    lower_list = []
    price_list = []
    last_sup = 0
    last_end = 0
    last_upper = 0
    last_lower = 0

    for i in range(len(merge_data_training)):
        # print(i)
        sup = merge_data_training['S_Sup'].iloc[i]
        end = merge_data_training['S_Sup'].iloc[i] - merge_data_training['S_Use'].iloc[i]
        price_ending_stock = -288.96 * np.log(0.000137 * np.array(end).astype(np.float)) + 251
        price_list.append(price_ending_stock)

        if sup == last_sup and end == last_end:
            upper_list.append(last_upper)
            lower_list.append(last_lower)

        else:
            last_sup = sup
            last_end = end

            upper, lower = price_range(end, sup, 2, 2500)
            upper_list.append(upper)
            lower_list.append(lower)

            last_upper = upper
            last_lower = lower

        price = merge_data_training['S_Close'].iloc[i]
        print(i, last_upper, price, last_lower)

    save_data_array = np.array([np.array(merge_data_training['Dates']), np.array(merge_data_training['S_Close']),
                               np.array(merge_data_training['S_Open']), np.array(upper_list), np.array(lower_list),
                                np.array(price_list)]).T
    save_data_pd = pd.DataFrame(save_data_array, columns=['Dates', 'S_Close', 'S_Open', 'upper', 'lower', 'ending'])
    save_data_pd.to_csv('soybeans_backtesting_data.csv', index=False)

    plt.plot(np.array(merge_data_training['S_Close']))
    plt.plot(upper_list, 'b')
    plt.plot(lower_list, 'g')
    plt.plot(np.array(price_list))

    plt.show()


if __name__ == '__main__':
    training_index = 2500
    #delayed_data_modification()
    #sup_computation(785, 4999, 2, training_index)
    #print(price_range(266, 3530, 3, training_index))
    prediction()
