from flask import Flask, redirect, render_template, request
<<<<<<< HEAD

from request_check import RequestCheck
=======
import request_check as check
>>>>>>> 05d6ca5f5d0deae181c2cdde48b68a99b4ece003
from db_editor import DatabaseEditor as D

app = Flask(__name__)
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
    db = D()
    check = RequestCheck()

    answer = True

    if request.method == "POST":
        answer = check.check_posted_request(request, db)
        path = f"/?found={answer}"
        return redirect(path)

    else:
        db.create_main_db()
        answer = get_answer(request)
        # print("Last_input: ", check.Last_input)
        # print("answer: ", answer)

        indata = list(db.select("SELECT * FROM weather ORDER BY n_id DESC"))

        if len(indata) == 10:
            db.delete(indata[-9][0])

<<<<<<< HEAD
        # print("indata[0] - ", indata) # indata[0]['weather']
        # {'n_id': 29, 'city': 'moscow', 'weather': 0.3}
=======
        # print("indata[0] - ", indata)
        # indata[0]['weather'] {'n_id': 29, 'city': 'moscow', 'weather': 0.3}
>>>>>>> 05d6ca5f5d0deae181c2cdde48b68a99b4ece003
        # indata[0] -  (1, 'moscow', -1.2)
        args = {"answer": answer, "last": check.Last_input, "indata": indata}

        return render_template("index.html", args=args)


if __name__ == "__main__":
    app.run()
