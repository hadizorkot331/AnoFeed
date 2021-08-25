from Home import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    password = db.Column(db.String(length=60), nullable=False)

class Messege(db.Model):
    messege_id = db.Column(db.Integer(), primary_key=True)
    messege = db.Column(db.String(length=240), nullable=False)
    time =db.Column(db.DateTime(), nullable=False)
    author = db.Column(db.Integer(), nullable=False)