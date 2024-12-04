# jinka/common/py/webscrape_connection.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from common.py.config import get_config

def get_driver():
    config = get_config()
    service = Service(config['chromedriver_path'])
    driver = webdriver.Chrome(service=service)
    return driver
