from flask import Flask, render_template, request, send_from_directory, redirect, jsonify
from flask_xmlrpcre.xmlrpcre import *
import os
import requests
import foodS_DB as db
import json
import datetime
from os.path import exists

app = Flask(__name__)

handler = XMLRPCHandler('api')
handler.connect(app, '/api')

@handler.register
def createRestaurant(name, room_id):
    if db.findRestaurant(name) == None:
        db.createRestaurant(name, room_id)
        url = "http://localhost:8000/api"
        data = {
            "link": "%s" % room_id
        }   
        headers = {
        "Content-Type": "application/json"
        }
        response = requests.post(url, json=data, headers=headers)
        print(response.status_code)
        print(response.json())

@handler.register
def validateRestaurant(name, owner):
    if db.findRestaurant(name) == None:
        return False
    else:
        return True
    
@handler.register
def myRestaurants(owner):
    print("Entrei aqui")
    restaurants = []
    for row in db.myRestaurants(owner):
        print (row.name)
        restaurants.append(row.name)
    print ("My restaurants:")
    print (restaurants)
    return restaurants

@handler.register
def updateMenu(name, menu):
    restaurant = db.findRestaurant(name)
    if restaurant != None:
        db.deleteMenu(restaurant.id)
    for item in menu:
        db.createMenu(item, restaurant.id)

@handler.register
def showReviews(name):
    restaurant = db.findRestaurant(name)
    if restaurant == None:
        return
    reviews = []
    for row in db.showReviews(restaurant.id):
        reviews.append(row.review)
    return reviews



@app.route('/')
@app.route('/index')
def index():
    restaurants = []
    for row in db.session.query(db.Restaurant):
        restaurants.append(row.name)
    return render_template('foodserviceapp.html', restaurants=restaurants)

@app.route('/restaurant/<name>')
def restaurant(name):
    return render_template('restaurant.html', restaurant=name)

@app.route('/restaurant/<name>/menu')
def menu(name):
    restaurant = db.findRestaurant(name)
    menu = []
    for row in db.session.query(db.Menu).filter_by(restaurant_id=restaurant.id):
        menu.append(row.item)
    return render_template('menu.html', menu=menu, restaurant=name)

@app.route('/restaurant/<name>/review', methods=['GET', 'POST'])
def review(name):
    if request.method == 'POST':
        restaurant = db.findRestaurant(name)
        review = db.Review(restaurant_id=restaurant.id, review=request.form['review'])
        db.session.add(review)
        db.session.commit()
        return redirect('/restaurant/%s' % name)
    else:
        return render_template('review.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)