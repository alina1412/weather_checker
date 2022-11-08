"""
application is one-paged
"""
from flask import redirect, render_template, request, session

from weather_app import app
from weather_app.config.config import Settings
from weather_app.db_editor import DatabaseEditor
from weather_app.logic import get_last_n_requests, processed_request


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = Settings().app_key


@app.route("/", methods=["GET", "POST"])
def index():
    db = DatabaseEditor()

    if request.method == "POST":
        session["last_input"], isfound = processed_request(request, db)
        return redirect(f"/?found={isfound}")
    else:
        isfound: bool = request.args.get("found") != "False"
        last_requests: list = get_last_n_requests(db)
        is_cold: bool = len(last_requests) > 0 and last_requests[0][1] < 1
        last_input: str = session.get("last_input", "")

        context = {
            "answer": isfound,
            "last": last_input,
            "indata": last_requests,
            "is_cold": is_cold,
        }
        return render_template("index.html", context=context)
