# -*- encoding: utf-8 -*-

"""Reddit Command Line Utilities."""

import os

__version__ = 'v0.1.11'

dir_path_to_conf = os.path.join(os.path.expanduser('~'), '.config/reclut')
if 'XDG_CONFIG_HOME' in os.environ:
    dir_path_to_conf = os.environ['XDG_CONFIG_HOME']

file_path_to_conf = os.path.join(dir_path_to_conf, 'config')
text = """
[account-info]
client_id = eIXXXXXXXXXX4g
client_secret = 1LXXXXXXXXXXXXXXXXXXXXXXX_s
password = 
username = 
user_agent = bot
"""

if not os.path.exists(dir_path_to_conf):
    os.makedirs(dir_path_to_conf)

if not os.path.exists(file_path_to_conf):
    with open(file_path_to_conf, 'w') as f:
        f.write(text)

