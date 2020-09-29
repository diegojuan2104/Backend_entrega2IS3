import sqlite3
from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    # db columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    preferences = db.Column(db.String(80))
    email = db.Column(db.String(80))
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))

    def __init__(self, username, password, preferences, email, name, lastname):
        self.username = username
        self.password = password
        self.email = email
        self.preferences = preferences
        self.name = name
        self.lastname = lastname

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"id": self.id,
                "username": self.username,
                "password":self.password,
                "preferences": self.preferences,
                "email": self.email,
                "name": self.name,
                "lastname": self.lastname,
                }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
