import platform
import os

def get_config_dir():
    if platform.system() == "Linux":
        if 'XDG_CONFIG_HOME' in os.environ:
            dir_path_to_conf = os.path.join(os.environ['XDG_CONFIG_HOME'], 'reclut')
        else:
            dir_path_to_conf = os.path.join(os.path.expanduser('~'), '.config/reclut')
    else:
        print("Not sure what to do on " + platform.system() + "... Exiting...")
        exit()
    return dir_path_to_conf


def get_config_path():
    return os.path.join(get_config_dir(), 'config')


def init_config(config_text):
    if not os.path.exists(get_config_dir()):
        os.makedirs(get_config_dir())

    if not os.path.exists(get_config_path()):
        with open(get_config_path(), 'w') as f:
            f.write(config_text)
