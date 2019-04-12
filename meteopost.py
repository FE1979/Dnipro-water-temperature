""" Basic functions for parsing
    https://meteopost.com/weather/archive/
"""

from bs4 import BeautifulSoup
import requests
import re
import time
# import plotly


def get_page(date):
    """ Reads review from meteopost.com
        :defaults: 'arc' - archive of the day, 'city' - UKKK - Zhulyany airport
        :input: date in time format
        :return: html page
    """

    URL = "https://meteopost.com/weather/archive/"
    d = ('0' + str(date.tm_mday))[-2:]
    m = ('0' + str(date.tm_mon))[-2:]
    y = str(date.tm_year)
    param = {'arc': '1', 'city': 'UKKK', 'd': str(d), 'm': str(m), 'y': str(y)}

    session = requests.Session()
    # session.verify = False
    t = session.post(URL, data=param)
    PAGE = t.text

    return PAGE

def get_weather_table(PAGE):
    """ Get weather archive table from a page
        :return:
        :rtype:
    """

    soup = BeautifulSoup(PAGE, 'html.parser')

    table = soup.find('table', id='arc')

    rows = table.find_all('tr')

    print(len(rows))

    for item in rows:
        colls = item.find_all('td')
        for val in colls:
            if val.text:
                print(val.text)
            else:
                img = val.find('img')
                print(img.attrs['title'])




page = get_page(time.localtime())
get_weather_table(page)
# print(page)
