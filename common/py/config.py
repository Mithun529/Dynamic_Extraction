# jinka/common/py/config.py
from configparser import ConfigParser

def get_config():
    config = ConfigParser()
    config.read('common/config/config.properties')
    return config['webdriver']
