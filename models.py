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

def get_all_people():
    characters = Character.query.all()
    serialized_characters = map(lambda character: character.serialize(), characters)
    if list(serialized_characters).count() > 0:
        return {"data": list(serialized_characters), "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Database empty"}
          
def get_person(person_id):
    characters = Character.query.all()
    serialized_characters = map(lambda character: character.serialize(), characters)
    filtered_characters = list(filter(lambda character: character['id'] == person_id, serialized_characters))
    if filtered_characters.count() > 0:
        return {"data": filtered_characters, "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Character id not valid"}  

def get_all_planets():
    planets = Planet.query.all()
    serialized_planets = map(lambda planet: planet.serialize(), planets)
    if list(serialized_planets).count() > 0:
        return {"data": list(serialized_planets), "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Database empty"}

def get_planet(planet_id):
    planets = Character.query.all()
    serialized_planets = map(lambda planet: planet.serialize(), planets)
    filtered_planets = list(filter(lambda planet: planet['id'] == planet_id, serialized_planets))
    if filtered_planets.count() > 0:
        return {"data": filtered_planets, "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Planet id not valid"} 

def get_all_users():
    users = User.query.all()
    serialized_users = map(lambda user: user.serialize(), users)
    if list(serialized_users).count() > 0:
        return {"data": list(serialized_users), "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Database empty"}

def get_favorites():
    fav_characters = Character.query.all()
    fav_planets = Planet.query.all()
    serialized_characters = map(lambda character: character.serialize(), fav_characters)
    serialized_planets = map(lambda planet: planet.serialize(), fav_planets)
    fav_list = list(serialized_characters) + list(serialized_planets)
    if list(fav_list).count() > 0:
        return {"data": list(fav_list), "status": 200 } 
    else: 
        return {"data": None, "status": 400, "message": "Database empty"}
    
def add_fav_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.add(planet)
    db.session.commit()
    fav_planets = UserFavPlanets.query.all()
    serialized_fav_planets = map(lambda fav_planet: fav_planet.serialize(), fav_planets)
    if list(serialized_fav_planets).count() > 0:
        return {"data": list(serialized_fav_planets), "status": 200}
    else:
        return {"data": None, "status": 400, "message": "No fav planets yet"}

def add_fav_person(character_id):
    character = Character.query.get(character_id)
    db.session.add(character)
    db.session.commit()
    fav_characters = UserFavCharacters.query.all()
    serialized_fav_characters = map(lambda fav_character: fav_character.serialize(), fav_characters)
    if list(serialized_fav_characters).count() > 0:
        return {"data": list(serialized_fav_characters), "status": 200}
    else:
        return {"data": None, "status": 400, "message": "No fav planets yet"}

def delete_fav_planet(planet_id):
    planet = Planet.query.get(planet_id)
    db.session.delete(planet)
    db.session.commit()
    fav_planets = UserFavPlanets.query.all()
    serialized_fav_planets = map(lambda fav_planet: fav_planet.serialize(), fav_planets)
    if list(serialized_fav_planets).count() > 0:
        return {"data": list(serialized_fav_planets), "status": 200}
    else:
        return {"data": None, "status": 400, "message": "No fav planets yet"}

def delete_fav_person(character_id):
    character = Character.query.get(character_id)
    db.session.delete(character)
    db.session.commit()
    fav_characters = UserFavCharacters.query.all()
    serialized_fav_characters = map(lambda fav_character: fav_character.serialize(), fav_characters)
    if list(serialized_fav_characters).count() > 0:
        return {"data": list(serialized_fav_characters), "status": 200}
    else:
        return {"data": None, "status": 400, "message": "No fav planets yet"}