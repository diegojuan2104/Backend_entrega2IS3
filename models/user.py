import sqlite3
from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    # db columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    preferences = db.Column(db.String(80))
    name = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    user_image_url = db.Column(db.String(120))

    def __init__(self, password, preferences, email, name, lastname,user_image_url):
        self.password = password
        self.email = email
        self.preferences = preferences
        self.name = name
        self.lastname = lastname
        self.user_image_url = user_image_url

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {"id": self.id,
                #"password":self.password,
                "preferences": self.preferences,
                "email": self.email,
                "name": self.name,
                "lastname": self.lastname,
                "user_image_url":self.user_image_url
                }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
