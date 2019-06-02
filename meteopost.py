""" Basic functions for parsing
    https://meteopost.com/weather/archive/
"""

from bs4 import BeautifulSoup
import requests
import re
import time
import json

#Global variables.
meteopost_file = 'meteopost_base.json'


def get_page(date):
    """ Reads review from meteopost.com
        :defaults: 'arc' - archive of the day, 'city' - UKKK - Zhulyany airport
        :input: date in time format
        :return: html page
    """

    URL = "https://meteopost.com/weather/archive/"
    d = str(date.tm_mday)[-2:]
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
        :return: text copy of weather archive table
        :rtype: list
    """

    soup = BeautifulSoup(PAGE, 'html.parser')

    table = soup.find('table', id='arc')
    rows = table.find_all('tr')

    weather_table = []

    for item in rows:
        colls = item.find_all('td')
        for val in colls:
            if val.text:
                weather_table[-1].append(val.text)
            else:
                img = val.find('img')
                weather_table[-1].append(img.attrs['title'])
        weather_table.append([])

    weather_table.pop()

    return weather_table

def transform_table(weather_table, date):
    """ Changes values of parsed table into usable types
        :input: weather_table
        :input: date of the report
        :return: transformed_weather_table
        :rtype: list
    """
    def get_number(string):
        """ gets only number from a string """
        regex = r'\d+'
        num_match = re.match(regex, string)
        return int(num_match.group())

    transformed_weather_table = []

    for item in weather_table:
        transformed_weather_table.append([])
        # get time
        regex = r'\d+:\d\d'
        time_match = re.match(regex, item[0])

        #make time stamp of the entry as epoch time
        time_string = time.strftime('%Y/%m/%d ', date) + time_match.group()
        epoch_time = time.mktime(time.strptime(time_string, '%Y/%m/%d %H:%M'))
        transformed_weather_table[-1].append(epoch_time)

        # get air temp
        air_temp = int(item[1][:-1]) # remove grade sign
        transformed_weather_table[-1].append(air_temp)

        # get pressure, wind direction, wind speed and humidity
        for i in range(2,6):
            transformed_weather_table[-1].append(get_number(item[i]))

        # get weather condition
        transformed_weather_table[-1].append(str(item[6]))

    return transformed_weather_table

def load_base():
    """ Loads meteopost database
        :rtype: list
    """

    with open(meteopost_file, 'r') as f:
        data = json.load(f)

    return data

def save_base(data):
    """ Saves database into a file
        :input: database
    """

    with open(meteopost_file, 'w') as f:
        json.dump(f, data)

def get_last_entry_time(data):
    """ Returns time stamp of last entry in base
        :rtype: float
    """

    return data[-1][0]

def run_meteopost(date=time.localtime()):
    """ Runs all scraping proccess
        :option by dafault: current date.
                            Specify another to scrap exact day data
        :return: weather data
        :rtype: list
    """
    page = get_page(date)
    weather_table =  get_weather_table(page)

    return transform_table(weather_table, date)

def run():
    """ Runs updating process from last date
        Note: runs only in same year
    """

    data_base = load_base()
    last_time = get_last_entry_time(data_base)

    #get timestamp as stuct_time
    last_entry_date = time.localtime(last_time)
    current_date = time.localtime()

    #get report for each day
    for i in range(last_entry_date.tm_yday, current_date.tm_yday):
        report_date = time.strptime(f"{report_date.tm_year} {i]", "%Y %j")
        meteo_report_table = run_meteopos(report_date)
        #append new data to the base. Existed entries will be overwritten
        data_base.update(meteo_report_table)
        #take a nap :)
        time.sllep(1)

    save_base(data_base)


if __name__ == "__main__":
    for item in run_meteopost():
        print(item)
