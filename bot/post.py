from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from bot.insta import RobotCore


class Post(RobotCore):
    """ handle all necessary posts methods"""
    def __init__(self,username, password):
        super(Post, self).__init__(username, password)

    def like_posts(self):
        ...


