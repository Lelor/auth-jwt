"""Blueprints for user transactions."""
from flask import Blueprint, request, jsonify, make_response

from api.modules.movie import save_object, get_genre_by_id, list_all_movies
from api.serializer.user import MOVIE_SERIALIZER, MOVIE_GENRE_SERIALIZER


bp = Blueprint('movies', __name__)


@bp.route("/movie", methods=["POST"])
def add_movie():
    """
    Movie registration route, the request must have the following fields:
        - name: str
        - release_date: datetime iso format
        - genre: integer (id of the movie genre)
        - director: str

    On success:
        Returns a success message, status 201.

    On request validation error:
        Returns an error message and a status of 400 (BAD REQUEST).

    On database integrity error:
        Returns an error message and a status of 409 (CONFLICT).
    """
    movie, err = MOVIE_SERIALIZER.load(request.json)
    if not get_genre_by_id(movie.genre_id):
        r = make_response(jsonify(message='invalid genre_id'))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 400
    if err:
        r = make_response(jsonify(err))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 400
    result = save_object(movie)

    if result:
        r = make_response(jsonify(message='success'))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 201

    r = make_response(
        jsonify(message='A conflict error ocurred in the database')
        )
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r, 409


@bp.route('/movie_genre', methods=['POST'])
def add_movie_genre():
    """
    Movie registration route, the request must have the following fields:
        - text: str

    On success:
        Returns a success message, status 201.

    On request validation error:
        Returns an error message and a status of 400 (BAD REQUEST).

    On database integrity error:
        Returns an error message and a status of 409 (CONFLICT).
    """
    genre, err = MOVIE_GENRE_SERIALIZER.load(request.json)
    if err:
        r = make_response(jsonify(err))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 400
    result = save_object(genre)

    if result:
        r = make_response(jsonify(message='success'))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 201

    r = make_response(
        jsonify(message='A conflict error ocurred in the database')
        )
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r, 409

@bp.route('/list_movies', methods=['GET'])
def list_movies():
    """
    Lists all movies found in the database
    """
    return list_all_movies(), 200
