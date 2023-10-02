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

@app.route("/check_in", methods=['GET', 'POST'])
def check_in():
    if request.method == 'GET':
        return render_template("check_in.html")
    else:
        print(request.form)
        place_id = request.form['place_id']
        user_id = request.form['user_id']
        timeofcheckin = datetime.datetime.now()
        timeofcheckout = None
        db.new_checkin(place_id, user_id, timeofcheckin, timeofcheckout)
        return redirect("/")
    
@app.route("/check_out", methods=['GET', 'POST'])
def check_out():
    if request.method == 'GET':
        return render_template("check_out.html")
    else:
        print(request.form)
        place_id = request.form['place_id']
        user_id = request.form['user_id']
        timeofcheckout = datetime.datetime.now()
        checkout_state = db.checkout(place_id, user_id, timeofcheckout)
        print(checkout_state)
        return redirect("/")