""" Basic functions for parsing
    https://meteo.gov.ua/ua//33345/hydrology/hydr_daily_situation
"""

from bs4 import BeautifulSoup
import requests
import re
import time


def get_page():
    """ Reads review from meteo.gov.ua
        :return: html page
    """

    URL = "https://meteo.gov.ua/ua//33345/hydrology/hydr_daily_situation"
    session = requests.Session()
    session.verify = False
    t = session.get(URL)
    PAGE = t.text

    return PAGE

def get_text(PAGE):
    """ Parse hydrology review from loaded page.
        Returns 'weekend', 'no data' if no report for this day.
        :input: loaded html page
        :return: review header and text
        :rtype: tuple
    """

    weekend_string = "У вихідні дні опис ситуації не оновлюється!"

    soup = BeautifulSoup(PAGE, "html.parser")

    main_text = soup.find('div', class_="cont_wr")
    main_text = main_text.find('div')
    main_text = main_text.find('div')

    if main_text.text == weekend_string:
        return 'weekend', 'no data'
    else:
        review_header = main_text.find('p').text
        return review_header, main_text.text


def get_water_temp(review_text):
    """ Gets water temperature from review
        :rtype: float
    """

    # get paragraph with temperature
    regex = r"Рівень.*Дніпро.*град."

    dnipro_match = re.search(regex, review_text)
    dnipro_info_string = review_text[dnipro_match.start():dnipro_match.end()]

    # remove all before temperature numbers
    regex = r"Рівень .+ дорівнювала "
    temp_string = re.sub(regex, '', dnipro_info_string)

    # get exactly numbers with possible delimiter
    regex = r"\d+\S*"
    temp_match = re.search(regex, temp_string)
    temperature = temp_string[temp_match.start() : temp_match.end()]

    # replace comma with point and convert to float
    regex = r","
    temperature = float(re.sub(regex, '.', temperature))

    return temperature

def get_reservoir_data(review_text):
    """ Get current filling of reservoirs
        :return: filling and free capacity
        :rtype: float
    """

    reservoir_capacity = 43.848

    regex = r"\d\d\W\d\d\d"

    reservoirs_fill = re.findall(regex, review_text)[0]

    regex = r","
    reservoirs_fill = float(re.sub(regex, '.', reservoirs_fill))

    reservoirs_free = reservoir_capacity - reservoirs_fill

    return reservoirs_fill, reservoirs_free

def get_review_date(review_header):
    """ Gets review date
        :return: numbers of a day, month and year
        :rtype: tuple
    """

    months = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
                'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']

    regex = r"год\."

    #get date_string
    date_pos = re.search(regex, review_header)
    date_string = review_header[date_pos.end() + 1:]
    #parse date text
    regex = r" "
    words = date_string.split(regex)

    day = words[0]
    month = str(months.index(words[1]) + 1)
    year = words[2]
    #convert text into time and return epoch time in sec
    date = '/'.join([day, month, year])
    date_struct = time.strptime(date, '%d/%m/%Y')

    return time.mktime(date_struct)


def run_meteo():
    """ Runs parsing meteo.gov.ua
        Returns 'weekend', 'no data' if no report for this day.
        :return: parsed data
        :rtype: tuple of hte next data:
            :date:              numbers tuple of day, month and year
            :water_temperature: float
            :reserve:           two floats - filling and free capacity
    """

    PAGE = get_page()
    review_data = get_text(PAGE)

    if review_data[0] != 'weekend':
        date = get_review_date(review_data[0])
        water_temperature = get_water_temp(review_data[1])
        reserve = get_reservoir_data(review_data[1])
        return date, water_temperature, reserve

    else:
        return review_data


if __name__ == "__main__":
    print(run_meteo())
