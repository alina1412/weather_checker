"""
application is one-paged
"""

from flask import redirect, render_template, request

from weather_app.db_editor import DatabaseEditor
from weather_app.logic import parse_args, processed_request

from weather_app import app

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    db = DatabaseEditor()
    isfound = True
    last_input = ""

    if request.method == "POST":
        last_input, isfound = processed_request(request, db)
        path = f"/?found={isfound}"
        return redirect(path)
    else:

        db.create_main_db()
        isfound = parse_args(request)

        indata = list(db.select("SELECT city, weather FROM weather ORDER BY n_id DESC"))
        if len(indata) == 10:
            db.delete(indata[-9][0])

        context = {"answer": isfound, "last": last_input, "indata": indata}
        print(last_input)
        return render_template("index.html", context=context)
