"""
application is one-paged
"""

from flask import redirect, render_template, request

from weather_app.db_editor import DatabaseEditor
from weather_app.request_check import RequestCheck

from weather_app import app

app.config["TEMPLATES_AUTO_RELOAD"] = True


def get_answer(request):
    get_found_s = request.args.get("found", type=str)
    if not get_found_s:
        answer = 1
    elif get_found_s.startswith("False"):
        answer = 0
    else:
        answer = 1
    return answer


@app.route("/", methods=["GET", "POST"])
def index():
    db = DatabaseEditor()
    check = RequestCheck()

    answer = True

    if request.method == "POST":
        answer = check.check_posted_request(request, db)
        path = f"/?found={answer}"
        return redirect(path)

    else:
        db.create_main_db()
        answer = get_answer(request)

        indata = list(db.select("SELECT city, weather FROM weather ORDER BY n_id DESC"))
        if len(indata) == 10:
            db.delete(indata[-9][0])

        args = {"answer": answer, "last": check.last_input, "indata": indata}
        return render_template("index.html", args=args)
