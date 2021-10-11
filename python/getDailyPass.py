#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import yaml

try:
    ff_opts = webdriver.FirefoxOptions()
    ff_opts.headless = True
    browser = webdriver.Firefox(options=ff_opts)
except Exception as err:
    print("Unable to initialize headless FireFox sessions with Selenium.")
    print(err)