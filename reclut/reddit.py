import os
from configparser import RawConfigParser

import praw


def reddit():
    config = RawConfigParser()
    config.read(f'{os.path.join(os.environ["HOME"], ".config/reclut/config")}')
    config = dict(config.items('account-info'))
    return praw.Reddit(client_id=config["client_id"],
                       client_secret=config["client_secret"],
                       password=config["password"], user_agent=config["user_agent"],
                       username=config["username"])
