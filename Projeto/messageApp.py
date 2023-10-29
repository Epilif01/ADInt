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
import message_DB as db
from os.path import exists

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("messageapp.html")


@app.route("/sendMessage", methods=["GET", "POST"])
def send_message():
    if request.method == "GET":
        return render_template("send_message.html")
    else:
        print(request.form)
        user_id = request.form["user_id"]
        message = request.form["message"]
        destination = request.form["destination"]
        db.new_message(user_id, message, destination)
        return redirect("/")


@app.route("/messagesSent", methods=["GET", "POST"])
def messages_sent():
    if request.method == "GET":
        return render_template("messages_sent.html")
    else:
        print(request.form)
        user_id = request.form["user_id"]
        messages = []
        for row in db.messages_sent(user_id):
            messages.append(row.message)
        print(messages)
        return render_template("show_message.html", messages=messages)


@app.route("/messagesReceived", methods=["GET", "POST"])
def messages_received():
    if request.method == "GET":
        return render_template("messages_received.html")
    else:
        print(request.form)
        user_id = request.form["user_id"]
        messages = []
        for row in db.messages_received(user_id):
            messages.append(row.message)
        print(messages)
        return render_template("show_message.html", messages=messages)

@app.route("/api/sendmessage/<user_id>", methods=["POST"])
def api_send_message(user_id):
    try:
        print("entrei aqui")
        print(request)
        message = request.json["message"]
        destination = request.json["destination"]
        print(message)
        print(destination)
        db.new_message(user_id, message, destination)
        return jsonify({"message": "Message sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/messagesreceived/<user_id>", methods=["GET"])
def api_messages_received(user_id):
    #user_id = request.form["user_id"]
    messages = []
    for row in db.messages_received(user_id):
        messages.append((row.sender,row.message))
    return jsonify(messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, debug=True)
