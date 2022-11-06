"""
application is one-paged
"""
import os

from flask import redirect, render_template, request, session

from weather_app import app
from weather_app.db_editor import DatabaseEditor
from weather_app.logic import processed_request

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SECRET_KEY"] = os.environ.get("app_key")


@app.route("/", methods=["GET", "POST"])
def index():
    db = DatabaseEditor()
    isfound = True

    if request.method == "POST":
        last_input, isfound = processed_request(request, db)
        session["last_input"] = last_input
        path = f"/?found={isfound}"
        return redirect(path)
    else:
        db.create_main_db()
        isfound = request.args.get("found") != "False"

        indata = list(db.select("SELECT city, weather FROM weather ORDER BY n_id DESC"))
        if len(indata) == 10:
            db.delete(indata[-9][0])
        is_cold = len(indata) > 0 and indata[0][1] < 1
        last_input = session.get("last_input", "")

        context = {
            "answer": isfound,
            "last": last_input,
            "indata": indata,
            "is_cold": is_cold,
        }
        return render_template("index.html", context=context)
