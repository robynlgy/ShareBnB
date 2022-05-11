import os

from flask import Flask, jsonify, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from pyparsing import token_map
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

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
app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)
jwt = JWTManager(app)

connect_db(app)
# db.drop_all()
db.create_all()


##############################################################################
# User signup/login/logout

@app.post('/signup')
def signup():
    """
    Create new user, add to DB and return token.

    Return error message if the there already is a user with that username.
    """
    username = request.json["username"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    password = request.json["password"]
    email = request.json["email"]
    image = request.json.get("image") or None

    try:
        token = User.signup(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
            image_url=image
        )
        db.session.commit()
        return jsonify({ "token": token })

    except IntegrityError:
        return jsonify({"error": "Username taken."})


@app.post('/login')
def login():
    """Return token upon authentication of user login."""

    token = User.authenticate(request.json["username"],request.json["password"])

    if token:
        return jsonify({ "token": token })

    return jsonify({"error": "Invalid login credentials."})


# POST /listing  -- accepts json
#   , auth: loggedIn
@app.post('/listings')
@jwt_required()
def post_listings():
    """
    Post listing and returns listing. Requires authentication.

    Accepts json :{name, image_url, price, location, details, listing_type}
    """
    username = get_jwt_identity()
    user = User.query.get(username)

    if not user:
        return jsonify({"error":"Access unauthorized."})

    listing = Listing.new(
        name = request.json["name"],
        image_url = request.json.get("image_url") or None,
        price = request.json["price"],
        location = request.json["location"],
        details = request.json["details"],
        listing_type = request.json["listing_type"],
        host_username = username
    )
    db.session.commit()

    return jsonify(listing=listing.serialize())


@app.get('/listings')
def get_listings():
    """ Get all listings. No authentication required. """

    listings = Listing.query.all()
    serialized = [listing.serialize() for listing in listings]

    return jsonify(listing=serialized)



# POST /messages/new -- accepts {message, to_user}
#  backend provide message_id, timestamp, from_id ,   auth: loggedIn