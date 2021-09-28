import configparser
import os


def get_config():
    try:
        env = os.environ.get("ENV", "DEV")
        if env =='LOCAL':
            config_file = os.path.join(os.environ.get("CONFIG_DIR"), "config.properties")
        elif env == 'DEV':
            config_file = os.path.join(os.environ.get("CONFIG_DIR"),"dev.config.properties")
        elif env == 'PRE':
            config_file = os.path.join(os.environ.get("CONFIG_DIR"), "pre.config.properties")
        elif env == 'PRO':
            config_file = os.path.join(os.environ.get("CONFIG_DIR"), "pro.config.properties")
        else:
            print("Not valid config")
        config = configparser.RawConfigParser()
        config.read(config_file)
    except Exception as e:
        print(e)
        print("Not valid config at {}".format(config_file))
    return config
