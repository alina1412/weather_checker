import requests

from weather_app.config.config import Settings


class WeatherFromApi:
    def __init__(self):
        self.openweather_api_key = Settings().openweather_api_key

    def get_temperature(self, city):
        url = "http://api.openweathermap.org" + f"/data/2.5/weather?q={city}"
        params = {"units": "metric", "appid": self.openweather_api_key}

        with requests.Session() as client:
            resp = client.get(url, params=params)
            data = resp.json()

            code = data.get("cod", None)
            if code == 401:
                print(data["message"])

            temperature = data.get("main", {}).get("temp", None)
            return temperature
