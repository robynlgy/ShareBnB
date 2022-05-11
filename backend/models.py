""" SQLAlchemy models for ShareB&B."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,JWTManager

DEFAULT_IMAGE_URL = "https://www.publicdomainpictures.net/pictures/280000/nahled/not-found-image-15383864787lu.jpg"

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    username = db.Column(
        db.Text,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )
    

    last_name = db.Column(
        db.Text,
        nullable=False,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(db.String,
                  nullable=False,
                  default=DEFAULT_IMAGE_URL)

    password = db.Column(
        db.Text,
        nullable=False,
    )

    # messages = db.relationship(
    #     'Message', secondary="users_messages", backref='users')

    # messages_sent = db.relationship(
    #     "User",
    #     secondary="users_messages",
    #     primaryjoin=(User_Message.from_username == username),
    #     secondaryjoin=(User_Message.to_username == username)
    # )
    #
    # messages_received = db.relationship(
    #     "User",
    #     secondary="users_messages",
    #     primaryjoin=(User_Message.to_username == username),
    #     secondaryjoin=(User_Message.from_username == username)
    # )

    listings = db.relationship('Listing', backref='user')

    def __repr__(self):
        return f"< User  #{self.username}: {self.first_name}, {self.last_name},{self.email} >"

    @classmethod
    def signup(cls, username, first_name, last_name, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        token = create_access_token(identity=username)

        db.session.add(user)
        return token

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                token = create_access_token(identity=username)
                return token

        return False


class Message(db.Model):
    """An individual message ("Share B&B")."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


class Listing(db.Model):
    """An individual listing ("Share B&B")."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    location = db.Column(
        db.Text,
        nullable=False,
    )

    details = db.Column(
        db.Text,
        nullable=False,
    )

    listing_type = db.Column(
        db.Text,
        nullable=False,
    )

    host_username = db.Column(
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )

    def __repr__(self):
        return f'< Listing  #{self.id}: {self.name}, ${self.price}, Location:{self.location}, Details:{self.details}, Listing type:{self.listing_type} >'

    @classmethod
    def new(cls, name, image_url, price, location, details, listing_type, host_username):
        """ Creates and returns new listing """

        listing = Listing(
           name=name,
           image_url=image_url,
           price=price,
           location=location,
           details=details,
           listing_type=listing_type,
           host_username=host_username
        )

        db.session.add(listing)
        return listing

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "name":self.name,
            "image_url":self.image_url,
            "price":self.price,
            "location":self.location,
            "details":self.details,
            "listing_type":self.listing_type,
            "host_username":self.host_username
        }



# class User_Message(db.Model):
#     """Join table between users and messages (the join represents a message)."""

#     __tablename__ = 'users_messages'

#     from_username = db.Column(
#         db.Text,
#         db.ForeignKey('users.username'),
#         nullable=False,
#         primary_key=True
#     )

#     to_username = db.Column(
#         db.Text,
#         db.ForeignKey('users.username', ondelete='CASCADE'),
#         nullable=False,
#         primary_key=True
#     )

#     message_id = db.Column(
#         db.Integer,
#         db.ForeignKey('messages.id', ondelete='CASCADE'),
#         nullable=False
#     )

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
