#!/usr/bin/env python3
from daily_pass_tools import LausdPass
from twilio.rest import Client
import yaml

# Retrieve secrets from yaml
secrets  = yaml.safe_load(open('login.yaml'))

# Grab login information
username   = secrets['user']['email']
password   = secrets['user']['password']
user_phone = secrets['user']['phone']

# Grab student information
student  = secrets['student']['name']
school   = secrets['student']['school']

# Grab Twilio information
account_sid  = secrets['twilio']['accountSID']
auth_token  = secrets['twilio']['authToken']
twilio_phone = secrets['twilio']['phone']

# Create a daily pass object
daily_pass = LausdPass(school_name=school, student_name=student)

# Login to daily pass site
daily_pass.navigate_to_pass_site()
daily_pass.log_into_pass_site(user=username, password=password)

# Generate daily pass QR code
daily_pass.create_daily_pass()
# daily_pass.qr_code

# Send QR code using Twilio SMS
print(f"Sending QR code to... {user_phone}")
message = f"Daily pass for {student} has been successfully generated. Please follow the link below...\n{daily_pass.qr_code}"
twilio_client = Client(account_sid, auth_token)
twilio_client.messages.create(
    to=user_phone,
    from_=twilio_phone,
    body=message
)