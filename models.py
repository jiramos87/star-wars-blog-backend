from re import M, S
from flask import jsonify, request, abort
import requests, json
from app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from requests.api import head
from app import db
import meta_weights
from flask_jwt_extended import create_access_token
from base64 import b64encode
import base64

baseUrl = 'https://futdb.app/api/players/search'
initial_meta_rating = 1
apiKey = '97c4dd2b-fe2e-4407-8ea3-f26435d6ce9b'



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(512))

    def __init__(self, username, email, password, is_admin):
        self.username = username
        self.email = email
        self.password = password
        self.is_admin = is_admin
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_admin": self.is_admin,
            "password": self.password
        }

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    home_planet = db.Column(db.Integer, nullable=False)

    def __init__(self, name, home_planet):
        self.name = name
        self.home_planet = home_planet

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "home_planet": self.home_planet
        }

class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation = db.Column(db.Integer, nullable=False)
    translation = db.Column(db.Integer, nullable=False)

    def __init__(self, name, rotation, translation):
        self.name = name
        self.rotation = rotation
        self.translation = translation

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation": self.rotation,
            "traslation": self.translation
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    vehicle_class = db.Column(db.String(250), nullable=False)
    weight = db.Column(db.Integer, nullable=False) 

    def __init__(self, name, vehicle_class, weight):
        self.name = name
        self.vehicle_class = vehicle_class
        self.weight = weight

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicle_class": self.vehicle_class,
            "weight": self.weight
        }

class UserFavCharacters(db.Model):
    __tablename__ = 'userfavcharacters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character = db.relationship("Character", back_populates="userfavcharacters" )
    user = db.relationship("User", back_populates="userfavcharacters")

    def __init__(self, name, character_id, user_id):
        self.name = name
        self.character_id = character_id
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "character_id": self.character_id,
            "user_id": self.user_id
        }


class UserFavPlanets(db.Model):
    __tablename__ = 'userfavplanets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet = db.relationship(Planet)

    def __init__(self, name, planet_id, user_id):
        self.name = name
        self.planet_id = planet_id
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "planet_id": self.character_id,
            "user_id": self.user_id
        }

class UserFavVehicles(db.Model):
    __tablename__ = 'userfavvehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    vehicle = db.relationship(Vehicle)

    def __init__(self, name, vehicles_id, user_id):
        self.name = name
        self.vehicles_id = vehicles_id
        self.user_id = user_id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "vehicles_id": self.vehicles_id,
            "user_id": self.user_id
        }