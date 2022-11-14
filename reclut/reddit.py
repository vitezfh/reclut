import os
import platform

from configparser import RawConfigParser

import praw

config = RawConfigParser()
# TODO:
#   check if platform.system() == "Linux"
#   then check if XDG_CONFIG_HOME defined and if not, store into home
#   TODO: [look into proper folder for this AND into output of cmd] if windows, then uhhh, whatever. Store into home 
#   TOOD: [look into it] if darwin, dunno. Probably also home
#   also create folders recursively and file too, with defaults
config.read(f'{os.path.join(os.environ["HOME"], ".config/reclut/config")}')
config = dict(config.items('account-info'))
reddit = praw.Reddit(client_id=config["client_id"],
                   client_secret=config["client_secret"],
                   password=config["password"], user_agent=config["user_agent"],
                   username=config["username"])
