""" SQLAlchemy models for ShareB&B."""

from cgitb import text
from datetime import datetime
from email import message

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity,JWTManager
from sqlalchemy import false

DEFAULT_IMAGE_URL = "https://st.depositphotos.com/1835047/1677/i/600/depositphotos_16770723-stock-photo-tree-house.jpg"
DEFAULT_USER_IMAGE_URL = "https://www.thepoke.co.uk/wp-content/uploads/2020/06/bread.jpg"

bcrypt = Bcrypt()
db = SQLAlchemy()

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
                  default=DEFAULT_USER_IMAGE_URL)

    password = db.Column(
        db.Text,
        nullable=False,
    )


    # messages_sent = db.relationship(
    #     "User",
    #     secondary="users_messages",
    #     primaryjoin=(User_Message.from_username == username),
    #     secondaryjoin=(User_Message.to_username == username)
    # )

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

    def serialize(self):
        """Serialize to dictionary."""

        return {
            "username":self.username,
            "firstName":self.first_name,
            "lastName":self.last_name,
            "email":self.email,
            "imageUrl":self.image_url,
        }


class Message(db.Model):
    """An individual message ("Share B&B")."""


    __tablename__ = 'messages'

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    # timestamp = db.Column(
    #     db.DateTime,
    #     nullable=False,
    #     default=datetime.utcnow(),
    # )

    recipient_id = db.Column(
        db.Text,
        primary_key=True,
    )
    
    def __repr__(self):
        return f'< Message  #{self.id}: {self.text}, ${self.recipient_id} >'
    
    @classmethod
    def new(cls, message, recipient):
        """ Creates and returns new message """

        message = Message(
            text=message,
            recipient_id=recipient
        )

        db.session.add(message)
        return message
    
    def serialize(self):
        """"Serialize"""
        
        return {
            "message":self.text,
            "recipient":self.recipient_id
        }

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

    @classmethod
    def edit(cls, name, image_url, price, location, details, listing_type, host_username):
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
            "id":self.id,
            "name":self.name,
            "imageUrl":self.image_url,
            "price":self.price,
            "location":self.location,
            "details":self.details,
            "listingType":self.listing_type,
            "hostUsername":self.host_username
        }




def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
