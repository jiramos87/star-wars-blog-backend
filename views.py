import requests
from flask import request, abort, send_from_directory
from models import get_all_people, get_person, get_all_planets, get_planet, get_all_users, get_favorites, add_fav_planet
from app import app

@app.route('/people', methods=['GET'])
def getallpeople():
    return get_all_people()

@app.route('/people/<int:person_id>', methods=['GET'])
def getperson(person_id):
    return get_person()

@app.route('/planets', methods=['GET'])
def getallplanets():
    return get_all_planets()

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getperson(planet_id):
    return get_planet()

@app.route('/users', methods=['GET'])
def getallusers():
    return get_all_users()

@app.route('/users/favorites', methods=['GET'])
def getfavorites():
    return get_favorites()

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addfavplanet(planet_id):
    return add_fav_planet(planet_id)