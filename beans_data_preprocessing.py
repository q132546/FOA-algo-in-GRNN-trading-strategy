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


def data_merge(training_index):
    s_p_data = pd.read_csv('soybeans_sup$use.csv')
    price_data = pd.read_csv('S1C1.csv')
    ending_quartly_data = pd.read_csv('S_ending_stock&quarterly_position.csv')
    fundamental_data = pd.merge(s_p_data, ending_quartly_data, on='Dates')
    merge_data = pd.merge(price_data, fundamental_data, on='Dates')

    return merge_data.iloc[:training_index], merge_data[training_index:]


def data_analysis():
    merge_data = data_merge(2300)
    released_date = Bloomberg_date_transformation()
    released_date_list = []

    for i in range(len(released_date)):

        released_date_list.append(np.where(merge_data['Dates'] == released_date[i])[0][0])

    x_name = 'S1_LAST'
    y_name = 'S_Sup'

    x = []
    y = []
    last_index = 0

    for i in range(len(released_date_list)):
        this_index = released_date_list[i]
        # x.append(merge_data[x_name].iloc[this_index] - merge_data[x_name].iloc[last_index])
        x.append(merge_data[x_name].iloc[this_index])
        # y.append(merge_data[y_name].iloc[this_index] - merge_data[x_name].iloc[last_index])
        y.append(merge_data[y_name].iloc[this_index] - merge_data['S_Use'].iloc[this_index])

        last_index = this_index

    print(stats.pearsonr(x, y))


def sup_computation(now_ending_stock, now_sup, selected_number, training_index):
    merge_data_training, merge_data_testing = data_merge(training_index)
    sup_list = []
    sup_price_dict = {}

    for i in range(len(merge_data_training)):
        sup = merge_data_training['S_Ending_stock'].iloc[i]
        price = merge_data_training['S1_LAST'].iloc[i]

        if sup not in sup_list:
            sup_list.append(sup)
            sup_price_dict[str(sup)] = []
            sup_price_dict[str(sup)].append(price)

        else:
            sup_price_dict[str(sup)].append(price)

    # regression

    keys = sup_price_dict.keys()
    target = []

    # plot
    for key in keys:
        target.append(np.mean(sup_price_dict[key]))

    target = np.array(target)
    x = np.array(list(keys))
    y = target
    sorted_y = []

    sorted_x = sorted(x)
    for x_index in range(len(x)):
        temp_index = np.where(x == sorted_x[x_index])[0][0]
        sorted_y.append(y[temp_index])

    reflected_line = -450 * np.log(0.0002 * np.array(sorted_x).astype(np.float))

    plt.scatter(sorted_x, reflected_line)
    plt.scatter(sorted_x, sorted_y)
    plt.xticks(fontsize=10, rotation=45)
    plt.show()

    # sort
    sorted_list = []
    combined_price = []
    diff_list = np.array(sup_list) - now_sup
    positive_list = diff_list[np.where(diff_list >= 0)[0]]
    negative_list = diff_list[np.where(diff_list < 0)[0]]
    print(positive_list)
    print(negative_list)
    for sort_index in range(selected_number):
        sorted_list.append(sorted(positive_list)[sort_index] + now_sup)
        sorted_list.append(sorted(negative_list)[-(sort_index + 1)] + now_sup)

    for i in range(len(sorted_list)):
        temp_list = sup_price_dict[str(sorted_list[i])]
        combined_price += temp_list
        print(np.mean(temp_list), np.std(temp_list), np.percentile(temp_list, 50))

    # combined prob computation
    print(np.mean(combined_price), np.std(combined_price), np.percentile(combined_price, 50))


def use_computation(now_use, selected_number, training_index):
    merge_data_training, merge_data_testing = data_merge(training_index)
    use_list = []
    use_price_dict = {}
    sup_use_diff = np.array(merge_data_training['S_Sup']) - np.array(merge_data_training['S_Use'])

    for i in range(len(merge_data_training)):
        use = sup_use_diff[i]
        price = merge_data_training['S1_LAST'].iloc[i]

        if use not in use_list:
            use_list.append(use)
            use_price_dict[str(use)] = []
            use_price_dict[str(use)].append(price)

        else:
            use_price_dict[str(use)].append(price)

    # sort
    sorted_list = []
    combined_price = []
    diff_list = np.array(use_list) - now_use
    positive_list = diff_list[np.where(diff_list >= 0)[0]]
    negative_list = diff_list[np.where(diff_list < 0)[0]]

    for sort_index in range(selected_number):
        sorted_list.append(sorted(positive_list)[sort_index] + now_use)
        sorted_list.append(sorted(negative_list)[-(sort_index + 1)] + now_use)

    # independent prob computation
    print(sorted(positive_list))
    print(use_price_dict)
    for i in range(len(sorted_list)):
        temp_list = use_price_dict[str(sorted_list[i])]
        combined_price += temp_list
        print(np.mean(temp_list), np.std(temp_list), np.percentile(temp_list, 50))

    print(np.mean(combined_price), np.std(combined_price), np.percentile(combined_price, 50))


def price_range(now_ending_stock, now_sup, selected_number, training_index):
    merge_data_training, merge_data_testing = data_merge(training_index)

    sup_list = []
    sup_price_dict = {}

    for i in range(len(merge_data_training)):
        sup = merge_data_training['S_Sup'].iloc[i]
        price = merge_data_training['S1_LAST'].iloc[i]

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
    print(diff_list)
    print(positive_list)
    print(sorted(negative_list))

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

    else:

        for sort_index in range(selected_number):
            sorted_list.append(sorted(positive_list)[sort_index] + now_sup)
            sorted_list.append(sorted(negative_list)[-(sort_index + 1)] + now_sup)

    for i in range(len(sorted_list)):
        print(sorted_list[i])
        temp_list = sup_price_dict[str(sorted_list[i])]
        combined_price += temp_list
        print(np.mean(temp_list), np.std(temp_list), np.percentile(temp_list, 50))

    # combined prob computation
    print(np.mean(combined_price), np.std(combined_price), np.percentile(combined_price, 50))

    price_ending_stock = 3880 - 480 * np.log(0.96 * np.array(now_ending_stock).astype(np.float))
    print(price_ending_stock)


if __name__ == '__main__':
    training_index = 2300
    sup_computation(785, 4999, 2, training_index)
    price_range(785, 4999, 2, training_index)

