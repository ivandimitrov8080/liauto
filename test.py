#!/usr/bin/env python

import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver

options = Options()
options.add_argument(r"user-data-dir=/home/ivand/.config/chromium")
options.add_argument(r"profile-directory=Profile 2")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options)
driver.implicitly_wait(1)

driver.get("https://the-internet.herokuapp.com/checkboxes")

el = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")

print(el[0].click())
time.sleep(5)
