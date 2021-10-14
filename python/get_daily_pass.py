#!/usr/bin/env python3
from daily_pass_tools import LausdPass
import yaml

# Retrieve secrets from yaml
secrets = yaml.safe_load(open('login.yaml'))
username = secrets['user']['email']
password = secrets['user']['password']
student  = secrets['student']['name']
school   = secrets['student']['school']

# Create a daily pass object
daily_pass = LausdPass(school_name=school, student_name=student)

# Login to daily pass site
daily_pass.navigate_to_pass_site()
daily_pass.log_into_pass_site(user=username, password=password)

daily_pass.create_daily_pass()
print(daily_pass.qr_code)