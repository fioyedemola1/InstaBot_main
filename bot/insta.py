import os
import time
import requests
import itertools
from selenium import webdriver
from bot.utility import search_btn
from typing import Optional, Sequence, List
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class Robot:
    BASE_URL: str = 'http://instagram.com'
    links: List = []

    def __init__(self, username: str, password: str):
        self.driver = webdriver.Chrome()
        self.username = username
        self.password = password
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
            password.send_keys(self.password)
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
                       limit: int = 10) -> WebDriver:
        """
        :param user:
        :param video:
        :param link:
        :param limit:
        :return:
        """

        _channel = '/channel/' if video else '/'  # ternary operator
        _user_url = f"{self.BASE_URL}/{user}{_channel}" if not link else link
        counter = itertools.count()
        condition = True if not link else False

        self.driver.get(_user_url)
        body = self.driver.find_element_by_tag_name('body')
        while condition:
            count = next(counter)
            time.sleep(1)
            body.send_keys(Keys.PAGE_DOWN)
            if count == limit:
                condition = False
        return body

    def get_pics(self,
                 user: str,
                 video: bool = False) -> List[str]:

        same_body = self.find_user_post(user, video)
        container = same_body.find_element_by_class_name('_2z6nI')
        a_tag = container.find_elements_by_tag_name('a')  # list
        linked = [x.get_attribute('href') for x in a_tag]  # ALL
        self.links = [*linked]
        return self.download(video=video)

    def download(self,
                 total=100,
                 video=True):  # video
        """function downloads video or image file from selected links generated from get_pics method """
        curr_mkdir = os.getcwd()
        vid_path = os.path.join(curr_mkdir, 'vid_file')
        os.makedirs(vid_path, exist_ok=True)
        content = '.mp4' if video else 'png'
        download_content = [x for x in os.listdir(vid_path) if x.endswith(content)]
        links = self.links
        if links:
            try:
                for num, link in enumerate(links):
                    self.driver.get(link)
                    if num <= total:
                        vid_link = self.driver.find_element_by_xpath('//video[@src]')
                        vid_url = vid_link.get_attribute('src')
                        re = requests.get(vid_url)
                        name = ''  # customise
                        content_name = f'{name}{num}.{content}'
                        if download_content:
                            if content_name in download_content:
                                continue
                        else:
                            with open(content_name, 'wb') as f:
                                f.write(re.content)
                    else:
                        break

            except Exception:
                raise NotImplemented

    @property
    def quit(self):
        return self.driver.quit()


def wrapped() -> None:
    ...


if __name__ == '__main__':
    wrapped()
