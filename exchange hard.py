# -*- coding: utf-8 -*-
import urllib.request
import json
from os.path import exists

currencies: dict[str, float] = {}  # Dictionary in which currencies will be added
URL: str = "https://www.cbr-xml-daily.ru/latest.js"


def get_currencies(link: str):
    """
    Get currencies and write in the currencies.txt file and currencies dictionary
    :return:
    """
    if exists('currencies.txt') is False:
        response = urllib.request.urlopen(link)
        data = json.loads(response.read())

        new_currencies = data[u'rates']

        with open('currencies.txt', 'w') as CURRENCIES_FILE:
            for line in new_currencies:
                CURRENCIES_FILE.write(line + ' ' + str(new_currencies[line]) + '\n')
        with open('currencies.txt', 'r') as CURRENCIES_FILE:
            for line in CURRENCIES_FILE:
                line = line.strip()
                file_split = line.split(' ')
                currencies[str(file_split[0])] = float(file_split[1])
    else:
        with open('currencies.txt', 'r') as CURRENCIES_FILE:
            for line in CURRENCIES_FILE:
                line = line.strip()
                file_split = line.split(' ')
                currencies[str(file_split[0])] = float(file_split[1])


def print_exchange_course():
    """
    Printing exchange course by 4 in row
    :return:
    """
    currencies_list = [[]]
    for key in currencies:
        if (len(currencies_list[len(currencies_list) - 1]) - 1) < 3:
            currencies_list[len(currencies_list) - 1].append(key + ': ' + str(round(currencies[key], 4)) + '  |  ')
        if (len(currencies_list[len(currencies_list) - 1]) - 1) == 3:
            currencies_list.append([])

    for i in currencies_list:
        result = ''.join(i)
        print(result)


def exchanger(value: str):
    """
    Separate query string, exchange and print result
    :param value:
    :return:
    """
    separate_quantity = value.split(' ')
    quantity, currency_from, currency_to = int(value.split(' ')[0]), separate_quantity[1].split('>')[0], \
        separate_quantity[1].split('>')[1]
    if currency_from == 'RUB':
        print('Result: ' + str(float(quantity)) + ' ' + str(currency_from) + ' = ' + str(
            round(quantity * currencies[currency_to], 2)) + ' ' + str(currency_to))
    elif currency_to == 'RUB':
        print('Result: ' + str(float(quantity)) + ' ' + str(currency_from) + ' = ' + str(
            round(quantity / currencies[currency_from], 2)) + ' ' + str(currency_to))
    else:
        print('Result: ' + str(float(quantity)) + ' ' + str(currency_from) + ' = ' + str(
            round((quantity / currencies[currency_from]) * currencies[currency_to], 2)) + ' ' + str(currency_to))


get_currencies(URL)
print_exchange_course()

# Transfer on next string and print tip and result while not 0 or empty
while True:
    try:
        print('')
        print('Query format: 100 USD>RUB')
        query = str(input('Input your query: '))  # '100 RUB>USD'
        if query != '0' and query != '':
            exchanger(query)
        else:
            break
    except Exception as e:
        print("Wrong query format!\n" + str(e))
        continue
