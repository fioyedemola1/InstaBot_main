from typing import NamedTuple, Optional


import os
import argparse

from dotenv import load_dotenv

from bot.insta import RobotCore
from bot.post import Post

load_dotenv()

USERNAME: Optional[str] = os.getenv('USERNAME')
PASSWORD: Optional[str]  = os.getenv('PASSWORD')


class UserDetails(NamedTuple):
    username: str
    password: str


args = argparse.ArgumentParser()
args.add_argument('-username', help='username or email', required=False)
args.add_argument('-password', help='password', required=False)


def user_info():
    """ Checks for user information passed either through command line or in .env file
    """
    cli = args.parse_known_args()[0]
    if cli.username and cli.password:
        user = UserDetails(cli.username, cli.password)
        return user
    else:
        if PASSWORD and USERNAME:
            user = UserDetails(USERNAME, PASSWORD)
            return user
        else:
            return NotImplemented ('You will need your log in details to progress')


if __name__ == '__main__':
    info = user_info()
    bob = Post(*info)
    bob.login()
    bob.like_posts()







