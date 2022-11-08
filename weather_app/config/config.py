import os


class Settings:
    openweather_api_key = os.environ.get("weather_api_key")
    app_key = os.environ.get("app_key")