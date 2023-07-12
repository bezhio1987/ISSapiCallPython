import time
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib

load_dotenv()

MY_LAT = 35.75679033696024
MY_LONG = 51.37579528257058

my_email = os.getenv('MY_EMAIL_USERNAME')
mailtrap_username = os.getenv('MAIL_TRAP_USERNAME')
mailtrap_password = os.getenv('MAIL_TRAP_PASSWORD')
mailtrap_host = os.getenv('MAIL_TRAP_HOST')

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


def send_email():
    with smtplib.SMTP(mailtrap_host, 2525) as server:
        server.connect(mailtrap_host, 2525)
        server.login(mailtrap_username, mailtrap_password)
        server.sendmail(from_addr=my_email,to_addrs=my_email, msg="Subject:Look Up \n\n The iSS is above")


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        send_email()
