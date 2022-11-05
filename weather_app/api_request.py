import os

import requests


class WeatherFromApi:
    def __init__(self):
        self.openweather_id = os.environ.get("weather_id")

    def get_temperature(self, city):
        url = "http://api.openweathermap.org" + f"/data/2.5/weather?q={city}"
        params = {"units": "metric", "appid": self.openweather_id}

        with requests.Session() as client:
            resp = client.get(url, params=params)
            data = resp.json()

            code = data.get("cod", None)
            if code == 401:
                print(data["message"])

            temperature = data.get("main", {}).get("temp", None)
            return temperature
