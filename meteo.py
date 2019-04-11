""" Basic functions for parsing
    https://meteo.gov.ua/ua//33345/hydrology/hydr_daily_situation
"""

from bs4 import BeautifulSoup
import requests
import re


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
    """ Parse hydrology review from loaded page
        :input: loaded html page
        :return: review header and text
        :rtype: tuple
    """

    soup = BeautifulSoup(PAGE, "html.parser")

    main_text = soup.find('div', class_="cont_wr")
    main_text = main_text.find('div')
    main_text = main_text.find('div')

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
        :return: filling
        :rtype: float
    """

    pass

def get_review_date(review_header):
    """ Gets review date
        :return: numbers of a day, month and year
        :rtype: tuple
    """
    months = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
                'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']

    regex = r"год\."

    date_pos = re.search(regex, review_header)
    date_string = review_header[date_pos.end() + 1:]

    regex = r" "
    words = date_string.split(regex)

    day = int(words[0])

    month = months.index(words[1]) + 1

    year = int(words[2])

    return day, month, year


t = get_text(get_page())
date = get_review_date(t[0])
wt = get_water_temp(t[1])
print(wt)
