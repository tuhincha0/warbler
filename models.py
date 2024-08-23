from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    likes = db.relationship('Message', secondary='likes', backref='liked_by')
    blocked = db.relationship('User', secondary='blocks', primaryjoin='User.id==Block.blocker_id', secondaryjoin='User.id==Block.blocked_id', backref='blocked_by')
    messages_sent = db.relationship('DirectMessage', foreign_keys='DirectMessage.sender_id')
    messages_received = db.relationship('DirectMessage', foreign_keys='DirectMessage.receiver_id')

class Message(db.Model):
    """Message model."""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sender = db.relationship('User', backref='sent_messages')

class Like(db.Model):
    """Like model."""

    __tablename__ = 'likes'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), primary_key=True)

class Block(db.Model):
    """Block model."""

    __tablename__ = 'blocks'
    blocker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

class DirectMessage(db.Model):
    """Direct message model."""

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def connect_db(app):
    db.app = app
    db.init_app(app)