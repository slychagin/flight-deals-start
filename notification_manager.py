import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

load_dotenv(override=True)

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.environ.get("TWILIO_VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.environ.get("TWILIO_VERIFIED_NUMBER")

MY_EMAIL = "slychagin@yahoo.com"
PASSWORD = os.environ.get("PASSWORD_YAHOO")

ENDPOINT = os.environ.get("SHEETY_USERS_ENDPOINT")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_message(self, message):
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_VIRTUAL_NUMBER,
            to=TWILIO_VERIFIED_NUMBER
        )
        print(message.sid)

    def send_emails(self, message, google_flight_link):
        response = requests.get(ENDPOINT)
        result = response.json()["users"]

        for user in result:
            with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=user["email"],
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode("utf-8")
                )
