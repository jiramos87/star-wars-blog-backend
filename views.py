import requests
from flask import request, abort, send_from_directory
from models import login, register, get_all_people, get_person, add_person, delete_person, update_person, get_all_planets, get_planet, add_planet, delete_planet, update_planet, get_all_users, get_favorites, add_fav_planet, add_fav_person, delete_fav_planet, delete_fav_person
from app import app

@app.route("/register", methods=['GET', 'POST'])
def register_fn():
    if request.method == 'POST':
        request_body = request.get_json()
        res = register(request_body)
        return res
        #return 'hola post'
    elif request.method == 'GET':
        return 'Hola GET'
    else:
        abort(405)


@app.route("/login", methods=["POST"])
def create_token():
    if request.method == 'POST':
        req_body = request.get_json()
        return login(req_body)
    elif request.method == 'GET':
        return 'This method only accepts POST'
    else:
        abort(405)

@app.route('/people', methods=['GET'])
def getallpeople():
    return get_all_people()

@app.route('/people/<int:person_id>', methods=['GET'])
def getperson(person_id):
    return get_person(person_id)

@app.route('/people', methods=['POST'])
def addperson():
    request_body = request.get_json()
    return add_person(request_body)

@app.route('/people', methods=['PUT'])
def updateperson():
    request_body = request.get_json()
    return update_person(request_body)

@app.route('/people', methods=['DELETE'])
def deleteperson():
    request_body = request.get_json()
    return delete_person(request_body)

@app.route('/planets', methods=['GET'])
def getallplanets():
    return get_all_planets()

@app.route('/planets/<int:planet_id>', methods=['GET'])
def getplanet(planet_id):
    return get_planet()

@app.route('/planets', methods=['POST'])
def addplanet():
    request_body = request.get_json()
    return add_planet(request_body)

@app.route('/planets', methods=['POST'])
def updateplanet():
    request_body = request.get_json()
    return update_planet(request_body)

@app.route('/planets', methods=['DELETE'])
def deleteplanet():
    request_body = request.get_json()
    return delete_planet(request_body)

@app.route('/users', methods=['GET'])
def getallusers():
    return get_all_users()

@app.route('/users/favorites', methods=['GET'])
def getfavorites():
    return get_favorites()

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addfavplanet(planet_id):
    return add_fav_planet(planet_id)

@app.route('/favorite/people/<int:person_id>', methods=['POST'])
def addfavperson(person_id):
    return add_fav_person(person_id)

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def deletefavplanet(planet_id):
    return delete_fav_planet(planet_id)

@app.route('/favorite/people/<int:person_id>', methods=['DELETE'])
def deletefavperson(person_id):
    return delete_fav_person(person_id)

