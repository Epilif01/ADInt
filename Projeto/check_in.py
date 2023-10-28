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


@app.route("/get_check_ins_outs", methods=["GET", "POST"])
def get_check_ins_outs():
    if request.method == "GET":
        return render_template("get_check_ins_outs.html")
    else:
        print(request.form)
        user_id = request.form["user_id"]
        return redirect("/list_check_ins_outs/" + user_id)


@app.route("/list_check_ins_outs/<path:user_id>")
def list_check_ins_outs(user_id):
    checkinsouts = db.getCheckinsouts(user_id)
    return render_template(
        "list_check_ins_outs.html", user_id=user_id, checkinsouts=checkinsouts
    )


@app.route("/api/check_in/<path:place_id>/<path:user_id>")
def check_inAPI(place_id, user_id):
    if db.getCheckin(user_id) is not None:
        return "User already checked in"
    timeofcheckin = datetime.datetime.now()
    timeofcheckout = None
    db.new_checkin(place_id, user_id, timeofcheckin, timeofcheckout)
    return jsonify({"status": "ok"})


@app.route("/api/check_out/<path:user_id>")
def check_outAPI(user_id):
    timeofcheckout = datetime.datetime.now()
    checkout_state = db.checkout(user_id, timeofcheckout)
    if checkout_state == "No checkin found":
        return "No checkin found"
    return jsonify({"status": "ok"})


@app.route("/api/checked_in/<path:place_id>")
def checked_inAPI(place_id):
    checked_in = db.getCheckedIn(place_id)
    return jsonify(checked_in)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003, debug=True)
