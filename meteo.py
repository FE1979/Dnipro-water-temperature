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
        :return: review text
        :rtype: str
    """

    soup = BeautifulSoup(PAGE, "html.parser")

    main_text = soup.find('div', class_="cont_wr")
    main_text = main_text.find('div')
    main_text = main_text.find('div')

    return main_text.text


def get_water_temp(review_text):
    """ Gets water temperature from review
        :rtype: float
    """

    pass

def get_reservoir_data(review_text):
    """ Get current filling of reservoirs
        :return: filling
        :rtype: float
    """

    pass

def get_review_date(review_text):
    """ Gets review date
        :rtype: time
    """

    pass



print(get_text(get_page()))
