import requests
from bs4 import BeautifulSoup
import datetime
import json
import smtplib
import time
import traceback
import random
from email.mime.text import MIMEText

POLL_INTERVAL = 60 * 60


def send_email(subject, body):
    mailconf = open("mail.txt", "r")
    from_user = mailconf.readline()
    from_password = mailconf.readline()
    to = mailconf.readline()

    message = MIMEText(body, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = from_user
    message['To'] = to

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(from_user, from_password)
    server.sendmail(from_user, to, message.as_string())
    server.close()
    print("email is sent")


def get_tiyatrolar_sessions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sessions = soup.find(id="activity_session").find_all('p')
    result = []
    for session in sessions:
        if "BİLET AL" in session.text:
            datestr = session.contents[1]
            datesplit = datestr.split()
            date = datetime.datetime.strptime("{} {}".format(datesplit[0], datesplit[3]), '%d.%m.%Y %H:%M')
            placestr = session.contents[-1].text
            datestr = date.strftime("%Y-%m-%d-%H-%M")
            result.append({"date" : datestr, "place" : placestr})
    return result


while True:
    try:
        while True:
            print("Check events {}".format(datetime.datetime.now()))
            with open('events.json', 'r', encoding='utf-8') as json_file:
                events = json.load(json_file)

            for event in events:
                tiyatrolar_sessions = get_tiyatrolar_sessions(event["url"])
                for tiyatrolar_session in tiyatrolar_sessions:
                    if tiyatrolar_session not in event["sessions"]:
                        print("New session is found for {}".format(event["url"]))
                        email_body="New session is found for:\nURL: {}\nDate: {}\nPlace: {}\n".format(event["url"], tiyatrolar_session["date"], tiyatrolar_session["place"])
                        send_email("New session is found", email_body)
                        print(tiyatrolar_session)
                        event["sessions"].append({"date" : tiyatrolar_session["date"], "place" : tiyatrolar_session["place"]})

            with open('events.json', 'w', encoding='utf-8') as json_file:
                json.dump(events, json_file, ensure_ascii=False, indent=4)

            time.sleep(POLL_INTERVAL + random.randint(0, 1000))

    except Exception as e:
        print(e)
        traceback.print_exc()
        time.sleep(POLL_INTERVAL)
