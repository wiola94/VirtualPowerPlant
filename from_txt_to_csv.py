import pandas as pd

if __name__ == '__main__':

    dates = pd.date_range(start='2017-01-01', end='2018-01-01', freq='h')
    dates = dates[:-1]

    full_prices = list()
    for file_number in range(1, 13):
        current_file = open('TGE txt/TGE_{}.txt'.format(file_number), 'r')
        lines = current_file.readlines()
        lines_numeric = list()
        for line in lines:
            lines_numeric.append(float(line[:-1]))
        current_file.close()
        print(lines_numeric)
        print(len(lines_numeric))
        full_prices += lines_numeric
    prices = pd.DataFrame(data=full_prices, index=dates)
    prices.to_csv('prices_year_new.csv')
