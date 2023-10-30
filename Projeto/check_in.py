from flask import (
    Flask,
    jsonify,
)
import datetime
import checkin_db as db

app = Flask(__name__)

@app.route("/api/check_in/<path:place_id>/<path:user_id>", methods=["POST"])
def check_inAPI(place_id, user_id):
    if db.getCheckin(user_id) is not None:
        return jsonify({"status": "User already checked in"})

    timeofcheckin = datetime.datetime.now()
    timeofcheckout = None
    db.new_checkin(place_id, user_id, timeofcheckin, timeofcheckout)
    return jsonify({"status": "ok"})


@app.route("/api/check_out/<path:user_id>", methods=["POST"])
def check_outAPI(user_id):
    timeofcheckout = datetime.datetime.now()
    checkout_state = db.checkout(user_id, timeofcheckout)
    if checkout_state == "No checkin found":
        return "No checkin found"
    return jsonify({"status": "ok"})


@app.route("/api/checked_in/<path:place_id>")
def checked_inAPI(place_id):
    checked_in = []
    for row in db.getCheckedIn(place_id):
        checked_in.append(row.user_id)

    return jsonify(checked_in)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003, debug=True)
