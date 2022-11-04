"""
Weather flask application
works with http://api.openweathermap.org
"""

# isort: skip_file
from flask import Flask


app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder="ui/templates",
    static_folder="ui/static",
)

import weather_app.views
