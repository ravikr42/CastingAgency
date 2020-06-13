from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, CHAR
import os

import app_utils

database_path = os.getenv("DATABASE_URL", "postgres://postgres:Welcome123@localhost:5432/casting_agency")

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    # db.drop_all()
    db.create_all()


'''
Model: Actors
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(CHAR(1), nullable=False)
    identifier = Column(String(36), unique=True, default=None)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f"Name: {self.name}, age: {self.age}"

    def format(self):
        gender = self.gender
        gen = 'Male'
        if gender == 'M':
            gen = 'Male'
        elif gender == 'F':
            gen = 'Female'
        else:
            gen = 'Unknown'
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': gen,
            'identifier': self.identifier
        }


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)
    production_house = Column(String(50))
    ott_partner = Column(String(20))
    identifier = Column(String(36), unique=True, default=None)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        f"Title: {self.title}, release_date: {self.release_date}"

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": app_utils.get_datetime_as_str(self.release_date),
            "production_house": self.production_house,
            "ott_partner": self.ott_partner,
            "identifier": self.identifier

        }
