import os

from flask import Flask, jsonify, request, flash
import flask
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from aws import send_to_s3
from models import db, connect_db, User, Listing, Message
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from flask_cors import CORS

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']
app.config['S3_BUCKET'] = os.environ["BUCKET_NAME"]
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(
    app.config['S3_BUCKET'])
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# toolbar = DebugToolbarExtension(app)
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
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    password = request.json["password"]
    email = request.json["email"]
    image = request.json.get("image") or None
    print('in backend signup')
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
        return jsonify({"token": token})

    except IntegrityError as e:
        return jsonify({"error": str(e)})


@app.post('/login')
def login():
    """Return token upon authentication of user login."""

    token = User.authenticate(
        request.json["username"], request.json["password"])

    if token:
        return jsonify({"token": token})

    return jsonify({"error": "Invalid login credentials."})


@app.get('/<username>')
@jwt_required()
def get_user(username):
    """Return user info. Requires authentication."""

    JWTusername = get_jwt_identity()

    user = User.query.get_or_404(username)

    if JWTusername != username:
        return jsonify({"error": "Unauthorized access."})

    serialized = user.serialize()
    return jsonify(user=serialized)


##############################################################################
# Listings

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
        return jsonify({"error": "Access unauthorized."})

    try:
        listing = Listing.new(
            name=request.json["name"],
            image_url=request.json.get("imageUrl") or None,
            price=request.json["price"],
            location=request.json["location"],
            details=request.json["details"],
            listing_type=request.json["listingType"],
            host_username=username
        )
        db.session.commit()

        return jsonify(listing=listing.serialize())
    except KeyError as e:
        print("keyerror>>>>>>", e)
        return jsonify({"error": f"Missing {str(e)}"})


@app.post('/listings/<int:id>/img')
@jwt_required()
def upload_image(id):
    """
    Post image and returns listing. Requires authentication.

    Accepts file: image_url
    """

    print('inside listing post<<<<<<<<')
    username = get_jwt_identity()
    user = User.query.get_or_404(username)
    listing = Listing.query.get_or_404(id)

    if not user:
        return jsonify({"error": "Access unauthorized."})

    file = request.files['File']
    if file:
        file.filename = secure_filename(file.filename)
        output = send_to_s3(file, app.config["S3_LOCATION"])
        listing.image_url = output
        db.session.commit()
        response = jsonify({"success": "image uploaded"})
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.get('/users/listings')
@jwt_required()
def get_listings_by_user():
    """ Get all listings by user. Must be logged in. """

    username = get_jwt_identity()
    user = User.query.get_or_404(username)

    listings = user.listings

    serialized = [listing.serialize() for listing in listings]
    return jsonify(listing=serialized)

@app.get('/listings')
def get_listings():
    """ Get all listings. No authentication required. """

    search_term = request.args.get('listing')

    if search_term:
        listings = Listing.query.filter_by(name=search_term)
    else:
        listings = Listing.query.all()

    print(listings)
    serialized = [listing.serialize() for listing in listings]
    return jsonify(listing=serialized)




@app.get('/listings/<int:id>')
def get_listing(id):
    """ Get all listing. No authentication required. """

    listing = Listing.query.get_or_404(id)
    serialized = listing.serialize()
    return jsonify(listing=serialized)

##############################################################################
# Messages
# POST /messages/new -- accepts {message,  recipient_id}
#  backend provide message_id, timestamp, from_id , recipient_id
@app.post('/messages')
@jwt_required()
def post_message():
    """ Post new message to another user.

    Accepts json {message, toUsername} """
    username = get_jwt_identity()
    user = User.query.get(username)

    if not user:
        return jsonify({"error": "Access unauthorized."})

    try:
        message = Message.new(
            message=request.json["message"],
            recipient=request.json["recipient"]
        )
        db.session.commit()

        return jsonify(message=message.serialize())
    except KeyError as e:
        print("keyerror>>>>>>", e)
        return jsonify({"error": f"Missing {str(e)}"})

    # TODO:
    # username = get_jwt_identity()
    # user = User.query.get_or_404(username)
    # text = request.json["text"]
    # to_username = request.json["to_username"]
    # message = Message(text=text)
    # db.session.add(message)

    # user.messages_sent.append()
