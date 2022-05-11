from distutils.log import error
import os

from flask import Flask, jsonify, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import db, connect_db, User, Listing
from dotenv import load_dotenv
load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)


@app.post('/signup')
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    email = request.json["email"]
    image = request.json.get("image") or None

    try:
        user = User.signup(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            image_url=image
        )
        db.session.commit()

    except IntegrityError as e:
        flash("Username already taken", 'danger')
        return jsonify({"error”: “username taken"})

    # do_login(user)


connect_db(app)
db.drop_all()
db.create_all()
