from os import environ


class Settings:
    openweather_api_key = environ.get("weather_api_key")
    app_key = environ.get("app_key")
