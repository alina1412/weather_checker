<<<<<<< HEAD
import os
import requests


class RequestCheck:

    def __init__(self):
        self.openweather_id = os.environ.get("weather_id")
        self.Last_input = ""

    def getTemperature(self, city):
        url = ("http://api.openweathermap.org" +
               f"/data/2.5/weather?q={city}")
        params = {"units": "metric", "appid": self.openweather_id}

        with requests.Session() as client:
            resp = client.get(url, params=params)
            data = resp.json()

            if data and "main" in data:
                return data["main"]["temp"]
            print("weather not found")
            return None

    def isEnglish(self, s):
        try:
            s.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            s = s.replace(" ", "")
            s = s.replace("-", "")
            return s.isalpha()

    def users_input(self, request):
        city = request.form.get("p-name", type=str)
        self.Last_input = city
        if self.isEnglish(city):
            # print("Eng")
            city = city.replace("-", " ")
            city = "+".join(city.split(" "))
            # Nizhny+Novgorod
            return city
        return ""

    def process(self, city, db):
        t_in_city = self.getTemperature(city)
        if t_in_city:
            weather = round(t_in_city, 1)
            query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
            db.run_query(query, (self.Last_input, weather))
            return True
=======
from http.client import HTTPSConnection
from json import loads

Last_input = ""


def getTemperature(city):
    c = HTTPSConnection("api.openweathermap.org")
    appid = "appid=cb37668bb0f9f472913ecc40fcb08884"
    c.request('GET', f'/data/2.5/weather?q={city}&units=metric&' + appid)
    res = c.getresponse()
    data = res.read()
    data = loads(data)
    # print(data)
    if data and "main" in data:
        return data["main"]["temp"]
    else:
        # print("not found")
        return None


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        s = s.replace(" ", "")
        s = s.replace("-", "")
        return s.isalpha()


def users_input(request):
    global Last_input
    city = request.form.get("p-name", type=str)
    Last_input = city
    if isEnglish(city):
        # print("Eng")
        city = city.replace("-", " ")
        city = "+".join(city.split(" "))
        # Nizhny+Novgorod
        return city


def check_posted_request(request, db):
    global Last_input
    city = users_input(request)
    # print("city--", city)
    if not city:
>>>>>>> 05d6ca5f5d0deae181c2cdde48b68a99b4ece003
        return False

    def check_posted_request(self, request, db):
        city = self.users_input(request)
        # print("city--", city)
        if city:
            return self.process(city, db)
        else:
            return False
