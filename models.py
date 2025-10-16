from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
db = SQLAlchemy()
class User(UserMixin, db.Model):
id = db.Column(db.Integer, primary_key=True)
2
username = db.Column(db.String(80), unique=True, nullable=False)
email = db.Column(db.String(200), unique=True, nullable=False)
password_hash = db.Column(db.String(200), nullable=False)
is_premium = db.Column(db.Boolean, default=False)
created_at = db.Column(db.DateTime, default=datetime.utcnow)
class Reservation(db.Model):
id = db.Column(db.Integer, primary_key=True)
user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
title = db.Column(db.String(200), nullable=False)
details = db.Column(db.Text, nullable=True)
created_at = db.Column(db.DateTime, default=datetime.utcnow)
user = db.relationship('User', backref='reservations')
