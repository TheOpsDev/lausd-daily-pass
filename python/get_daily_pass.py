#!/usr/bin/env python3
from yaml import tokens
from daily_pass_tools import LausdPass
from twilio.rest import Client
from bitlyshortener import Shortener
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
twilio_auth_token = secrets['twilio']['authToken']
account_sid  = secrets['twilio']['accountSID']
twilio_phone = secrets['twilio']['phone']

# Grab Bitly information
bitly_auth_token = secrets['bitly']['authToken']

# Create a daily pass object
daily_pass = LausdPass(school_name=school, student_name=student)

# Login to daily pass site
daily_pass.navigate_to_pass_site()
daily_pass.log_into_pass_site(user=username, password=password)

# Generate daily pass QR code
daily_pass.create_daily_pass()
# daily_pass.qr_code

# Generate a Bit.ly link for QR code
# Required workaround for Twilio's character limit
bitly = Shortener(tokens=[bitly_auth_token])
short_url = bitly._shorten_url(daily_pass.qr_code)

# Send QR code using Twilio SMS
print(f"Sending QR code to... {user_phone}")
message = f"Daily pass for {student} has been successfully generated. Please follow the link below...\n{short_url}"
twilio_client = Client(account_sid, twilio_auth_token)
twilio_client.messages.create(
    to=user_phone,
    from_=twilio_phone,
    body=message
)
