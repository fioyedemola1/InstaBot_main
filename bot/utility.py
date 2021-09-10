import itertools
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver


class Html:
    pass


def search_btn(x: WebDriver):
    return x.find_element(By.CLASS_NAME, 'bIiDR')


def get_html_content(body: WebDriver):
    html: Html = body.get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def pacer(pace: int) ->None:
    return time.sleep(pace)
