from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    jsonify,
)
import os
import datetime
import checkin_db as db
from os.path import exists

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("check_in_app.html")


@app.route("/check_in", methods=["GET", "POST"])
def check_in():
    if request.method == "GET":
        return render_template("check_in.html")
    else:
        print(request.form)
        place_id = request.form["place_id"]
        user_id = request.form["user_id"]
        if db.getCheckin(user_id) is not None:
            return redirect("/check_in_failed/" + place_id)

        timeofcheckin = datetime.datetime.now()
        timeofcheckout = None
        db.new_checkin(place_id, user_id, timeofcheckin, timeofcheckout)
        return redirect("/")


@app.route("/check_out", methods=["GET", "POST"])
def check_out():
    if request.method == "GET":
        return render_template("check_out.html")
    else:
        print(request.form)
        user_id = request.form["user_id"]
        timeofcheckout = datetime.datetime.now()
        checkout_state = db.checkout(user_id, timeofcheckout)
        print(checkout_state)
        if checkout_state == "No checkin found":
            return redirect("/check_out_failed")
        return redirect("/")


@app.route("/check_out_failed")
def check_out_failed():
    return render_template("check_out_failed.html")


@app.route("/check_in_failed/<path:place_id>")
def check_in_failed(place_id):
    return render_template("check_in_failed.html", place_id=place_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003, debug=True)
