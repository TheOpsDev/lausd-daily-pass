#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import yaml
import time

# Create headless firefox session
try:
    ff_opts = webdriver.FirefoxOptions()
    ff_opts.headless = True
    browser = webdriver.Firefox(options=ff_opts)
except Exception as err:
    print("Unable to initialize headless FireFox session with Selenium.")
    print(err)

# Navigate to parents login page
browser.get('https://pap.lausd.net/en-US/SignIn')
parent_sign_in = browser.find_element(By.ID, 'https://idcs-5143070ce03d415eb20fdc5866138826.identity.oraclecloud.com/')
parent_sign_in.send_keys(Keys.RETURN)

# Time delay to allow page load
time.sleep(5)

# Grab form elements for login
username_form = browser.find_element(By.ID, 'idcs-signin-basic-signin-form-username')
password_form = browser.find_element(By.ID, 'idcs-signin-basic-signin-form-password|input')
sign_in_btn   = browser.find_element(By.ID, 'idcs-signin-basic-signin-form-submit')

# Retrieve credentials from yaml
creds = yaml.safe_load(open('login.yaml'))
username = creds['lausd_user']['email']
password = creds['lausd_user']['password']

# input credential information
username_form.send_keys(username)
password_form.send_keys(password)
sign_in_btn.click()

# Check if vaccine prompt is shown at login
try:
    vaccine_prompt = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/button')
    vaccine_prompt.click()
except Exception as err:
    print("No vaccine prompt, continuing execution")
    print(err)

# click Get Daily Pass button
get_pass_btn = browser.find_element(By.ID, 'create_pass')
get_pass_btn.click()

time.sleep(5)

# Select student
student_btn = browser.find_element(By.XPATH, '/html/body/div[5]/button[2]')
student_btn.click()

time.sleep(5)

# Provide school information
school_form = browser.find_element(By.ID, 'facility')
school_form.send_keys('LORNE STREET ELEMENTRY')
school_btn = browser.find_element(By.XPATH, '/html/body/form/div[5]/button')

# sympton/contact validation
symptons_radio_btn = browser.find_element(By.ID, 'anycovid19symptoms_0')
contact_radio_btn = browser.find_element(By.ID, 'contactwithCOVID19case_0')
symptons_radio_btn.click()
contact_radio_btn.click()