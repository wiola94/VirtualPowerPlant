from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta

d1 = date(2017, 10, 1)  # start date
d2 = date(2017, 10, 31)  # end date

delta = d2 - d1         # timedelta

for i in range(delta.days + 1):
    current_date = d1 + timedelta(i)

    if current_date.day == 1:
        whole_prices_in_month = list()
        month_file = open('TGE_{}.txt'.format(current_date.month), 'w')

    response = requests.get('https://gaz.tge.pl/pl/rdn/tgebase/?date={}'.format(current_date))
    soup = BeautifulSoup(response.content, 'html.parser')
    stat_table = soup.find_all('table', class_='t-02')
    stat_table = stat_table[0]

    r = 0
    prices_one_day = list()
    for row in stat_table.find_all('tr', class_='prices'):
        c = 0
        if r != 0:
            for cell in row.find_all('td'):
                if c == 1:
                    prices_one_day.append(cell.text)
                c += 1
        r += 1

    prices_one_day = prices_one_day[1:]
    prices_one_day_numeric = list()

    for elem in prices_one_day:
        try:
            str_elem = float(elem[1:-1])
        except ValueError:
            str_elem = 0
        prices_one_day_numeric.append(str_elem)

    if current_date.month == 10 and current_date.day == 28:
        prices_one_day_numeric = prices_one_day_numeric[:2] + prices_one_day_numeric[3:]

    print(len(prices_one_day_numeric))

    # print(prices_one_day_numeric)
    # print(len(prices_one_day))
    whole_prices_in_month += prices_one_day_numeric
    print(current_date.day)

    next_date = d1 + timedelta(i+1)
    if current_date.day != next_date.day and next_date.day == 1:
        for elem in whole_prices_in_month:
            month_file.write('{}\n'.format(elem))
        month_file.close()
