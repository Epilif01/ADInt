from flask import Flask, render_template, request, send_from_directory, redirect, jsonify
from flask_xmlrpcre.xmlrpcre import *
import requests
import roomS_DB as db

app = Flask(__name__)

handler = XMLRPCHandler("api")
handler.connect(app, "/api")


@handler.register
def createRoom(name, owner):
    if db.findRoom(name) == None:
        db.createRoom(name, owner)

@handler.register
def realRoom(room_id):
    url = " https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/%s" % room_id 
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return jsonify(data)
        else:
            return jsonify({"error": "Failed to fetch data from the API"}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@handler.register
def validateRoom(name, owner):
    if db.findRoom(name) == None:
        return False
    else:
        return True


@handler.register
def myRooms(owner):
    rooms = []
    for row in db.myRooms(owner):
        print(row.name)
        rooms.append(row.name)
    print(rooms)
    return rooms


@handler.register
def updateSchedule(name, weekday, slot_start, slot_end):
    room = db.findRoom(name)
    if room != None:
        db.deleteSchedule(room.id)
    db.createSchedule(weekday, slot_start, slot_end, room.id)


@app.route("/")
@app.route("/index")
def index():
    rooms = []
    for row in db.session.query(db.Room):
        rooms.append(row.name)
    return render_template("roomserviceapp.html", rooms=rooms)


@app.route("/room/<name>")
def room(name):
    return render_template("room.html", room=name)


@app.route("/room/<name>/schedule")
def schedule(name):
    room = db.findRoom(name)
    schedule = []
    for row in db.session.query(db.Schedule).filter_by(room_id=room.id):
        schedule.append((row.weekday, row.slot_start, row.slot_end))
    return render_template("schedule.html", schedule=schedule, room=name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True)
