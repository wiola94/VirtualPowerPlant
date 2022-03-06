import pandas as pd
import matplotlib.pyplot as plt
import operator


def get_reload_indexes():
    energy_prices = pd.read_csv('prices_year.csv', index_col=[0], parse_dates=[0])
    energy_prices_list = energy_prices['0'].values.tolist()
    reload_indexes = []
    max_indexes = []
    for index, price in enumerate(energy_prices_list):
        if index % 24 == 4:
            beginning = index
            end = index + 24
            max_index, max_value = max(enumerate(energy_prices_list[beginning:end]), key=operator.itemgetter(1))
            max_indexes.append(max_index)
            reload_indexes.append(beginning + max_index - 3)
    return max_indexes, reload_indexes


if __name__ == '__main__':
    m_indexes, r_indexes = get_reload_indexes()
    plt.hist(m_indexes, bins=24)
    plt.show()