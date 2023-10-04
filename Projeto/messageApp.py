from flask import Flask, render_template, request, send_from_directory, redirect, jsonify
import os
import datetime
import checkin_db as db
from os.path import exists

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template("check_in_app.html")

@app.route("/send_message", methods=['GET', 'POST'])
def send_message():
    if request.method == 'GET':
        return render_template("send_message.html")
    else:
        print(request.form)
        user_id = request.form['user_id']
        message = request.form['message']
        destination = request.form['destination']
        db.new_message(user_id, message, destination)
        return redirect("/")