import itertools

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bot.hasher import Protector
from bot.utility import search_btn, pacer
from typing import Optional, List
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait



class RobotCore(Protector):
    BASE_URL: str = 'http://instagram.com'
    links: List = []

    def __init__(self, username: str, password: str):
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = self.encrypt(password)
        self.driver.get(self.BASE_URL)
        # self.driver.maximize_window()

    @property
    def _cookie(self):
        self.driver.implicitly_wait(10)

        try:
            WebDriverWait(self.driver, timeout=10).until(search_btn).click()
        except TimeoutException:
            return None

    def login(self):
        """

        """
        self._cookie
        username = WebDriverWait(self.driver, timeout=10).until(lambda x: x.find_element_by_name('username'))
        password = WebDriverWait(self.driver, timeout=10).until(lambda x: x.find_element_by_name('password'))
        if username and password:
            username.send_keys(self.username)
            password.send_keys(self.decrypt(self.password))
        else:
            return

        login_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
        login_btn.click()

        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//*[contains(text(),'Not now')]")).click()
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//*[contains(text(),'Not Now')]")).click()

    def find_user_post(self, user: str,
                       video: bool = False,
                       link: Optional[str] = None,
                       limit: int = 10) -> None:

        _channel = '/channel/' if video else '/'  # ternary operator
        _user_url = f"{self.BASE_URL}/{user}{_channel}" if not link else link
        condition = True if not link else False

        self.driver.get(_user_url)
        self.scroller(limit, condition=condition)

    def scroller(self, limit: int = 1, condition: bool = True ) -> None:
        counter = itertools.count()
        while condition:
            count = next(counter)
            pacer(1.5)
            body = self.driver.find_element_by_tag_name('body')
            body.send_keys(Keys.PAGE_DOWN)
            if count == limit:
                condition = False
#
# def wrapped() -> None:
#     ...
#
#
# if __name__ == '__main__':
#     wrapped()

    @property
    def quit(self):
        return self.driver.quit()






