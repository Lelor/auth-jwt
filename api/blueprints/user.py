"""Blueprints for user transactions."""
from flask import Blueprint, request, jsonify, make_response

from api.modules.validators import validate_token
from api.modules.user import registrate_user, authenticate
from api.serializer.user import (USER_AUTH_SERIALIZER,
                                 USER_REGISTRATION_SERIALIZER)


bp = Blueprint('users', __name__)


@bp.route("/user", methods=["POST"])
def add_user():
    """
    User creation route, the request must have the following fields:
        - username: str
        - email: str
        - password: str

    On success:
        Returns a success message and an active token with 20 minutes
        of duration, status 201.

    On request validation error:
        Returns an error message and a status of 400 (BAD REQUEST).

    On database integrity error:
        Returns an error message and a status of 409 (CONFLICT).
    """
    user, err = USER_REGISTRATION_SERIALIZER.load(request.json)
    if err:
        r = make_response(jsonify(err))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 400
    result = registrate_user(user)

    if result:
        r = make_response(jsonify(message='success',
                                  token=user.generate_token()))
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 201

    r = make_response(jsonify(message='user already registered'))
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r, 409


@bp.route("/sign_in", methods=["POST"])
def sign_in():
    """
    Authentication route, the request must have the following fields:
        - username: str
        - password: str

    On success:
        Returns a success message and an active token with 20 minutes
        of duration, status 200

    On invalid credentials:
        Returns a error message and a status of 401 (FORBIDDEN)

    On request validation error:
        Returns an error message and a status of 400 (BAD REQUEST).
    """

    err = USER_AUTH_SERIALIZER.validate(request.json)
    if err:
        r = jsonify(err)
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 400
    token = authenticate(request.json['username'],
                         request.json['password'])
    if token:
        r = jsonify(message='success', token=token)
        r.headers["Access-Control-Allow-Origin"] = '*'
        return r, 200
    r = make_response(jsonify(message='invalid credentials'))
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r, 401


@bp.route('/secret', methods=['GET'])
@validate_token
def super_secret_route(token):
    """
    Route to exemplify the use of an authenticated endpoint.
    """
    return jsonify(message='super secret message', decoded_token=token)
