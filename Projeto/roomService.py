from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    jsonify,
)
from flask_xmlrpcre.xmlrpcre import *
import requests
import roomS_DB as db

app = Flask(__name__)

handler = XMLRPCHandler("api")
handler.connect(app, "/api")


@handler.register
def createRoom(name, room_id):
    if db.findRoom(room_id) == None:
        db.createRoom(name, room_id)
        url = "http://localhost:8000/api"
        data = {"link": "s%s" % room_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        print(response.status_code)
        print(response.json())
        new_url = "http://localhost:8000/files/%s" % response.json()["filename"]
        return new_url


@handler.register
def updateFromFenix(room_id):
    url = " https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/%s" % room_id

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            updateSchedule(room_id, data["events"])
        else:
            return jsonify({"error": "Failed to fetch data from the API"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@handler.register
def validateRoom(room_id):
    if db.findRoom(room_id) == None:
        return False
    else:
        return True


@handler.register
def myRooms():
    rooms = []
    for row in db.myRooms():
        print(row.name)
        rooms.append(row.name)
    print(rooms)
    return rooms


@handler.register
def updateSchedule(room_id, data):
    room = db.findRoom(room_id)
    if room != None:
        db.deleteSchedule(room_id)

    db.createSchedule(room_id, data)


@app.route("/")
@app.route("/index")
def index():
    rooms = []
    for row in db.session.query(db.Room):
        rooms.append((row.name, row.room_id))
    return render_template("roomserviceapp.html", rooms=rooms)


@app.route("/room/<room_id>")
def room(room_id):
    return render_template("room.html", room_id=room_id)


@app.route("/room/<room_id>/schedule")
def schedule(room_id):
    room = db.findRoom(room_id)
    schedule = []
    for row in db.session.query(db.Schedule).filter_by(room_id=room_id):
        schedule.append((row.weekday, row.slot_start, row.slot_end))
    return render_template("schedule.html", schedule=schedule, room_id=room_id)


@app.route("api/<room_id>/schedule")
def scheduleAPI(room_id):
    schedule = []
    for row in db.session.query(db.Schedule).filter_by(room_id=room_id):
        schedule.append((row.weekday, row.slot_start, row.slot_end))
    return jsonify(schedule)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
