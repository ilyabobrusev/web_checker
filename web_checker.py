#!/usr/bin/python3
import urllib.request
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# read setting file
settings = "settings.ini"
config = configparser.ConfigParser(interpolation=None)
config.read(settings)

# config parameters
# web
url = (config["web"]["url"])
# file with validation status
info_file = (config["file"]["info_file"])
# email
email_server = (config["email"]["email_server"])
sender = (config["email"]["sender"])
password = (config["email"]["password"])
recipient = (config["email"]["recipient"])
message = (config["email"]["message"])
subject = (config["email"]["subject"])


# read check info file
def check_info_file(*args):
    try:
        file = open(*args, "r+")
    except FileNotFoundError:
        print("info_file not exist")
        exit(0)
    try:
        return [i.strip() for i in file.readlines()]
    finally:
        file.close()


# get url status code func
def get_status_code(*args):
    try:
        status_code = urllib.request.urlopen(*args).getcode()
    except urllib.error.URLError:
        status_code = 0
    return status_code


# write check info file
def write_info_file():
    f = open('info_file', 'w')
    f.write(str(get_status_code(url)))
    f.close()


# send email func
def send_mail():
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    # add in the message body
    msg.attach(MIMEText(url + "\n" + message, 'plain'))
    server = smtplib.SMTP(email_server)
    # server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


if get_status_code(url) == 200 and int(check_info_file(info_file)[0]) == 0:
    write_info_file()


if get_status_code(url) == 0 and int(check_info_file(info_file)[0]) == 200:
    write_info_file()
    send_mail()
