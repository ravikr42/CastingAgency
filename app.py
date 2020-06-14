import sys

from flask import Flask, request, abort, jsonify, redirect
from flask_cors import CORS
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth

import app_utils
from models.dbmodel import setup_db, Actor, Movie, db_drop_and_create_all, db

RESULTS_PER_PAGE = 6

app = Flask(__name__)
setup_db(app)
migrate = Migrate(app, db)
db_drop_and_create_all()
CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,DELETE')
    return response


@app.route("/")
@app.route("/health")
@app.route("/status")
def app_greet():
    message = {
        "message": "Welcome to Casting Agency"
    }
    return jsonify(message)


@app.route("/actors", methods=['POST'])
@requires_auth('add:actors')
def create_actors(jwt):
    error = False
    try:
        data = request.get_json()
        actor = Actor(name=data['name'], age=data['age'])
        actor.identifier = app_utils.generate_guid()
        if data['gender'] is not None:
            if data['gender'].lower() == 'male':
                actor.gender = 'M'
            elif data['gender'].lower() == 'female':
                actor.gender = 'F'
            else:
                actor.gender = 'U'
        actor.insert()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        abort(422)

    if not error:
        result = {
            'success': True,
            'id': actor.id,
            'identifier': actor.identifier
        }
    return jsonify(result)


@app.route("/movies", methods=['POST'])
@requires_auth('add:movie')
def create_movies(jwt):
    error = False
    try:
        data = request.get_json()
        movie = Movie(title=data['title'],
                      production_house=data['production_house'],
                      ott_partner=data['ott_partner'])
        movie.release_date = app_utils.get_datetime(data['release_date'])
        movie.identifier = app_utils.generate_guid()
        movie.insert()
        print(data)
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        abort(422)

    if not error:
        result = {
            "success": True,
            "id": movie.id,
            "identifier": movie.identifier
        }

    return jsonify(result)


@app.route("/actors")
@requires_auth('get:actors')
def get_all_actors(jwt):
    actors = Actor.query.all()
    if len(actors) == 0:
        abort(404)
    result = {
        "success": True,
        "actors": paginate_actors(actors),
        'page': request.args.get('page', 1, type=int)
    }
    return jsonify(result)


def paginate_actors(selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    actors = list(map(Actor.format, selection))
    current_actors = actors[start:end]
    return current_actors


def paginate_movies(selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    movies = list(map(Movie.format, selection))
    current_movies = movies[start:end]
    return current_movies


@app.route("/movies")
@requires_auth('get:movie')
def get_all_movies(jwt):
    movies = Movie.query.all()
    if len(movies) == 0:
        abort(404)
    result = {
        "success": True,
        "actors": paginate_movies(movies),
        'page': request.args.get('page', 1, type=int)
    }
    return jsonify(result)


@app.route("/actors/<int:actor_id>")
@requires_auth('get:actors')
def get_actor_info(jwt, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).first()
    if actor is None:
        abort(404)
    result = {
        "success": True,
        "actor_details": actor.format()
    }
    return jsonify(result)


@app.route("/movies/<int:movie_id>")
@requires_auth('get:movie')
def get_movie_info(jwt, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).first()
    if movie is None:
        abort(404)
    result = {
        "success": True,
        "movie_details": movie.format()
    }
    return jsonify(result)


@app.route("/actors/<int:actor_id>", methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    error = False
    try:
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        actor.delete()
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

    if not error:
        result = {
            "success": True,
            "actor_id": actor.id,
            "status": "Deleted"
        }
    return jsonify(result)


@app.route("/movies/<int:movie_id>", methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(jwt, movie_id):
    error = False
    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(404)
        movie.delete()
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
        abort(422)

    if not error:
        result = {
            "success": True,
            "movie_id": movie.id,
            "status": "Deleted"
        }
    return jsonify(result)


@app.route("/actors/<int:actor_id>", methods=['PATCH'])
@requires_auth('modify:actors')
def update_actor_info(jwt, actor_id):
    error = False
    try:
        actor = Actor.query.filter(Actor.id == actor_id).first()
        if actor is None:
            abort(404)
        data = request.get_json()
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            if data['gender'].lower() == 'male':
                actor.gender = 'M'
            elif data['gender'].lower() == 'female':
                actor.gender = 'F'
            else:
                actor.gender = 'U'
        actor.update()
    except:
        error = True
        abort(422)
    if not error:
        result = {
            "success": True,
            "actor_id": actor.id
        }
    return jsonify(result)


@app.route("/movies/<int:movie_id>", methods=['PATCH'])
@requires_auth('modify:movie')
def update_movie_info(jwt, movie_id):
    error = False
    try:
        movie = Movie.query.filter(Movie.id == movie_id).first()
        if movie is None:
            abort(404)
        data = request.get_json()
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = app_utils.get_datetime(data['release_date'])
        if 'production_house' in data:
            movie.production_house = data['production_house']
        if 'ott_partner' in data:
            movie.ott_partner = data['ott_partner']
        movie.update()
    except:
        error = True
        abort(422)
    if not error:
        result = {
            "success": True,
            "movie_id": movie.id
        }
    return jsonify(result)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Invalid Request: There is problem with your input data"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "error": 404,
            "message": "Request resource not found"
        }
    ), 404


# Error Handler for Token Validations, verification errors
@app.errorhandler(AuthError)
def auth_error(error):
    response = jsonify(error.error)
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
