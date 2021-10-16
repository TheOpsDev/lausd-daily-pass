#!/usr/bin/env python3

from daily_pass_tools import LausdPass
import yaml

# Retrieve secrets from yaml
secrets  = yaml.safe_load(open('login.yaml'))

# Grab login information
username = secrets['user']['email']
password = secrets['user']['password']
phone    = secrets['user']['phone']

# Grab student information
student  = secrets['student']['name']
school   = secrets['student']['school']

# Create a daily pass object
daily_pass = LausdPass(school_name=school, student_name=student)

# Login to daily pass site
daily_pass.navigate_to_pass_site()
daily_pass.log_into_pass_site(user=username, password=password)

# Generate daily pass QR code
daily_pass.create_daily_pass()

# Share daily pass to user phone number
daily_pass.share_daily_pass(phone)