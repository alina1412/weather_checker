import os

import requests


class RequestCheck:
    def __init__(self):
        self.openweather_id = os.environ.get("weather_id")
        self.last_input = ""

    def get_temperature(self, city):
        url = "http://api.openweathermap.org" + f"/data/2.5/weather?q={city}"
        params = {"units": "metric", "appid": self.openweather_id}

        with requests.Session() as client:
            resp = client.get(url, params=params)
            data = resp.json()

            code = data.get("cod", None)
            if code == 401:
                print(data["message"])

            if data and "main" in data:
                return data["main"]["temp"]
            print("weather not found")
            return None

    def is_english(self, phrase):
        try:
            phrase.encode(encoding="utf-8").decode("ascii")
        except UnicodeDecodeError:
            return False
        else:
            phrase = phrase.replace(" ", "")
            phrase = phrase.replace("-", "")
            return phrase.isalpha()

    def users_input(self, request):
        city = request.form.get("p-name", type=str)
        self.last_input = city
        if self.is_english(city):
            city = city.replace("-", " ")
            city = "+".join(city.split(" "))
            # Nizhny+Novgorod
            return city
        return ""

    def process(self, city, db):
        t_in_city = self.get_temperature(city)
        if t_in_city:
            weather = round(t_in_city, 1)
            query = "INSERT INTO weather (city, weather) VALUES(?, ?)"
            db.run_query(query, (self.last_input, weather))
            return True
        return False

    def check_posted_request(self, request, db):
        city = self.users_input(request)
        if city:
            return self.process(city, db)
        return False
