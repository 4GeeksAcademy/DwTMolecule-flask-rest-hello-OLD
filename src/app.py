"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, FavoritePlanet, People, FavoritePeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/test', methods=['GET'])
def test():

    response_body = {
        "msg": "Esto es una prueba "
    }

    return jsonify(response_body), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets= Planet.query.all()
    print(all_planets)
    result= list(map(lambda planet: planet.serialize(),all_planets))
    print(result)

    response_body = {
        "msg": "Estoy trayendo planetas",
        "planets": result
    }

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    print(planet_id)
    # get the user with id 5
    planet = Planet.query.get(planet_id)
    print(planet)
   

    response_body = {
        "msg": "Estoy trayendo planeta",
        "planet": planet.serialize()
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_planet(planet_id,user_id):
    favorite_planet = FavoritePlanet(id_user=user_id, id_planet=planet_id)
    db.session.add(favorite_planet)
    db.session.commit()
    response_body = {
        "msg": "Voy a crear un planeta favorito "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_peoples():
    all_peoples= People.query.all()
    print(all_peoples)
    result= list(map(lambda planet: planet.serialize(),all_peoples))
    print(result)

    response_body = {
        "msg": "Estoy trayendo personajes",
        "planets": result
    }

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    print(people_id)
    # get the user with id 5
    people = People.query.get(people_id)
    print(people)
   

    response_body = {
        "msg": "Estoy trayendo un personaje",
        "people": people.serialize()
    }

    return jsonify(response_body), 200


@app.route('/favorite/people/<int:people_id>/user/<int:user_id>', methods=['POST'])
def add_favorite_people(people_id,user_id):
    favorite_people = FavoritePeople(id_user=user_id, id_people=people_id)
    db.session.add(favorite_people)
    db.session.commit()
    response_body = {
        "msg": "Voy a crear un personaje favorito a este usuario "
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    all_users= User.query.all()
    print(all_users)
    result= list(map(lambda user: user.serialize(),all_users))

    response_body = {
        "msg": "Estoy trayendo usuarios",
        "users": result
    }

    return jsonify(response_body), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    print(user_id)
    # get the user with id 5
    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="user not found"), 404

    favorite_people = FavoritePeople.query.filter_by(id_user=user_id).all()
    serialized_favorite_people = [favorite.serialize() for favorite in favorite_people]
   

    response_body = {
        "msg": "Estoy trayendo un usuario y sus favoritos",
        "people": serialized_favorite_people
    }

    return jsonify(response_body), 200


@app.route('/favorite/people/<int:people_id>', methods= ["DELETE"])
def delete_favorite_people(people_id):

    user_id= 1
    exist = FavoritePeople.query.filter_by(id_user= user_id, id_people= people_id).first()
    if exist :
        db.session.delete(exist)
        db.session.commit()
    return jsonify({"msg": "Personaje eliminado de los favoritos"})


@app.route('/favorite/planet/<int:planet_id>', methods= ["DELETE"])
def delete_favorite_planet(planet_id):

    user_id= 1
    exist = FavoritePlanet.query.filter_by(id_user= user_id, id_planet= planet_id).first()
    if exist :
        db.session.delete(exist)
        db.session.commit()
    return jsonify({"msg": "Planeta eliminado de los favoritos"})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
