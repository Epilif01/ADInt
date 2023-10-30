import os
import secrets
from urllib.parse import urlencode

from dotenv import load_dotenv
from flask import (
    Flask,
    redirect,
    url_for,
    render_template,
    flash,
    session,
    current_app,
    request,
    abort,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
import requests

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["OAUTH2_PROVIDERS"] = {
    "fenix": {
        "client_id": os.environ.get("FENIX_CLIENT_ID"),
        "client_secret": os.environ.get("FENIX_CLIENT_SECRET"),
        "authorize_url": "https://fenix.tecnico.ulisboa.pt/oauth/userdialog",
        "token_url": "https://fenix.tecnico.ulisboa.pt/oauth/access_token",
        "userinfo": {
            "url": "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person",
            "email": lambda json: json["email"],
        },
        "scopes": [],
    },
}

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "index"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    istid = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    token = db.Column(db.String(300))


class Enrollments(db.Model):
    __tablename__ = "enrollments"
    id = db.Column(db.Integer, primary_key=True)
    courseid = db.Column(db.Integer, nullable=False)
    istid = db.Column(db.String(64), nullable=False)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


@app.route("/")
def index():
    return render_template("app_index.html")


@app.route("/other")
def other_route():
    try:
        response = requests.get(
            "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person",
            headers={
                "Authorization": "Bearer " + current_user.token,
                "Accept": "application/json",
            },
        )
        if response.status_code != 200:
            abort(401, "not authorized")
        user_info = response.json()

        print(user_info)
        return "returned name " + user_info["name"]
    except:
        abort(401, "not logged in in FLASK")


@app.route("/api/<user_id>/courses")
def coursesAPI(user_id):
    data = db.session.query(Enrollments).filter_by(istid=user_id)
    courses = []
    for row in data:
        courses.append(row.courseid)
    return jsonify(courses)


@app.route("/api/<room_id>/menu", methods=["GET"])
def menuAPI(room_id):
    return jsonify(
        requests.get(
            "http://localhost:8001/api/%s/menu" % room_id,
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/api/<room_id>/review/<user_id>", methods=["POST"])
def evaluateAPI(room_id, user_id):
    try:
        review = request.json["review"]

        response = requests.post(
            "http://localhost:8001/api/%s/review/%s" % (room_id, user_id),
            json={
                "review": review,
            },
            headers={"Content-Type": "application/json"},
        )

        # Return the response from the Send Messages Server to the browser
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/<room_id>/schedule")
def schedule(room_id):
    return jsonify(
        requests.get(
            "http://localhost:8002/api/%s/schedule" % room_id,
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/api/sendmessage/<user_id>", methods=["POST"])
def api_send_message(user_id):
    try:
        message = request.json["message"]
        destination = request.json["destination"]

        response = requests.post(
            "http://localhost:8004/api/sendmessage/%s" % user_id,
            json={"message": message, "destination": destination},
            headers={"Content-Type": "application/json"},
        )
        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/messagesreceived/<user_id>", methods=["GET"])
def api_messages_received(user_id):
    return jsonify(
        requests.get(
            "http://localhost:8004/api/messagesreceived/%s" % user_id,
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/api/check_in/<path:place_id>/<path:user_id>", methods=["POST"])
def check_inAPI(place_id, user_id):
    return jsonify(
        requests.post(
            "http://localhost:8003/api/check_in/%s/%s" % (place_id, user_id),
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/api/check_out/<path:user_id>", methods=["POST"])
def check_outAPI(user_id):
    return jsonify(
        requests.post(
            "http://localhost:8003/api/check_out/%s" % user_id,
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/api/checked_in/<path:place_id>")
def checked_inAPI(place_id):
    return jsonify(
        requests.get(
            "http://localhost:8003/api/checked_in/%s" % place_id,
            headers={
                "Accept": "application/json",
            },
        ).json()
    )


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))


@app.route("/authorize/<provider>")
def oauth2_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    # generate a random string for the state parameter
    session["oauth2_state"] = secrets.token_urlsafe(16)

    # create a query string with all the OAuth2 parameters
    qs = urlencode(
        {
            "client_id": provider_data["client_id"],
            "redirect_uri": url_for(
                "oauth2_callback", provider=provider, _external=True
            ),
            "response_type": "code",
            "scope": " ".join(provider_data["scopes"]),
            "state": session["oauth2_state"],
        }
    )

    # redirect the user to the OAuth2 provider authorization URL
    return redirect(provider_data["authorize_url"] + "?" + qs)


@app.route("/callback/<provider>")
def oauth2_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for("index"))

    provider_data = current_app.config["OAUTH2_PROVIDERS"].get(provider)
    if provider_data is None:
        abort(404)

    # if there was an authentication error, flash the error messages and exit
    if "error" in request.args:
        for k, v in request.args.items():
            if k.startswith("error"):
                flash(f"{k}: {v}")
        return redirect(url_for("index"))

    # make sure that the state parameter matches the one we created in the
    # authorization request
    if request.args["state"] != session.get("oauth2_state"):
        abort(401)

    # make sure that the authorization code is present
    if "code" not in request.args:
        abort(401)

    # exchange the authorization code for an access token
    response = requests.post(
        provider_data["token_url"],
        data={
            "client_id": provider_data["client_id"],
            "client_secret": provider_data["client_secret"],
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": url_for(
                "oauth2_callback", provider=provider, _external=True
            ),
        },
        headers={"Accept": "application/json"},
    )
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get("access_token")
    print(oauth2_token)
    if not oauth2_token:
        abort(401)

    # use the access token to get the user's email address
    response = requests.get(
        "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person",
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
    )
    if response.status_code != 200:
        abort(401)
    email = provider_data["userinfo"]["email"](response.json())
    print(response)
    istid = response.json()["username"]

    # find or create the user in the database
    user = db.session.scalar(db.select(User).where(User.email == email))
    if user is None:
        user = User(
            email=email, username=email.split("@")[0], istid=istid, token=oauth2_token
        )
        db.session.add(user)
        db.session.commit()

    response = requests.get(
        "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/person/courses",
        headers={
            "Authorization": "Bearer " + oauth2_token,
            "Accept": "application/json",
        },
    )
    if response.status_code != 200:
        abort(401)
    courses = response.json()["enrolments"]
    for course in courses:
        courseid = course["id"]
        enroll = db.session.scalar(
            db.select(Enrollments).where(Enrollments.courseid == courseid)
        )
        if enroll is None:
            enroll = Enrollments(courseid=courseid, istid=istid)
            db.session.add(enroll)
            db.session.commit()

    # log the user in
    login_user(user)
    return redirect(url_for("index"))


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
