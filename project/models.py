# models.py
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    credential = db.relationship('Credential', backref='user')

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credential_name = db.Column(db.String(100), nullable=False)
    credential_key = db.Column(db.String)
    credential_description = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    