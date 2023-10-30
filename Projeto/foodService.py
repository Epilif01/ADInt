from flask import (
    Flask,
    request,
    jsonify,
)
from flask_xmlrpcre.xmlrpcre import *
import requests
import foodS_DB as db

app = Flask(__name__)

handler = XMLRPCHandler("api")
handler.connect(app, "/api")


@handler.register
def createRestaurant(name, room_id):
    if db.findRestaurant(room_id) == None:
        db.createRestaurant(name, room_id)
        url = "http://localhost:8000/api"
        data = {"link": "r%s" % room_id}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=data, headers=headers)
        print(response.status_code)
        print(response.json())
        new_url = "http://localhost:8000/files/%s" % response.json()["filename"]
        return new_url


@handler.register
def validateRestaurant(room_id):
    if db.findRestaurant(room_id) == None:
        return False
    else:
        return True


@handler.register
def myRestaurants():
    restaurants = []
    for row in db.myRestaurants():
        print(row.name)
        restaurants.append(row.name)
    print("My restaurants:")
    print(restaurants)
    return restaurants


@handler.register
def updateMenu(room_id, menu):
    restaurant = db.findRestaurant(room_id)
    if restaurant != None:
        db.deleteMenu(room_id)
    for item in menu:
        db.createMenu(item, room_id)


@handler.register
def showReviews(room_id):
    restaurant = db.findRestaurant(room_id)
    if restaurant == None:
        return
    reviews = []
    for row in db.showReviews(room_id):
        reviews.append(row.review)
    return reviews

@app.route("/api/<room_id>/menu", methods=["GET"])
def menuAPI(room_id):
    restaurant = db.findRestaurant(room_id)
    menu = []
    for row in db.session.query(db.Menu).filter_by(restaurant_id=restaurant.room_id):
        menu.append(row.item)

    return jsonify({"name": restaurant.name, "menu": menu})


@app.route("/api/<room_id>/review/<user_id>", methods=["POST"])
def reviewAPI(room_id, user_id):
    restaurant = db.findRestaurant(room_id)
    review = db.Review(
        restaurant_id=restaurant.room_id, review=request.json["review"], user_id=user_id
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
