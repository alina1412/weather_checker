from flask import Flask
from flask import redirect, render_template, request 
# from flask import url_for, flash, jsonify, session
import db_check as check
from db_editor import DatabaseEditor as D

app = Flask(__name__) 
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'super secret key'

def before_request():
    app.jinja_env.cache = {}


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
    answer = True
    app.before_request(before_request)

    if request.method == "POST":
        answer  = check.cpost(request, db)
        path = f"/?found={answer}"
        return redirect(path)

    else:
        db.create_main_db()
        answer = get_answer(request)

        print("Last_input: ", check.Last_input)
        print("answer: ", answer)
        # num_rows = list(db.get_count())[0][0]
        # print("get_count: ", )

        indata = list(db.select("SELECT * FROM weather ORDER BY n_id DESC")) # [::-1]
        
        if len(indata) == 10: 
            db.delete(indata[-9][0])

        # print("indata[0] - ", indata) # indata[0]['weather'] {'n_id': 29, 'city': 'moscow', 'weather': 0.3}
        # indata[0] -  (1, 'moscow', -1.2)
        args = {"answer": answer, "last": check.Last_input, "indata": indata}

        return render_template("index.html", args=args)
        # return render_template("index.html", answer=answer, last=check.Last_input, indata=indata)





if __name__ == "__main__":
    app.run()