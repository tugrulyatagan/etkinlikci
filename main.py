import requests
from bs4 import BeautifulSoup
import datetime
import json


def get_tiyatrolar_sessions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    sessions = soup.find(id="activity_session").find_all('p')
    for session in sessions:
        if "BİLET AL" in session.text:
            datestr = session.contents[1]
            datesplit = datestr.split()
            date = datetime.datetime.strptime("{} {}".format(datesplit[0], datesplit[3]), '%d.%m.%Y %H:%M')
            placestr = session.contents[3].text
            print("{}  {}".format(date, placestr))


url = "https://tiyatrolar.com.tr/tiyatro/bir-baba-hamlet"
url = "https://tiyatrolar.com.tr/tiyatro/cimri5"
#get_tiyatrolar_sessions(url)


with open('etkinlikler.json') as json_file:
    data = json.load(json_file)
    print(data)