from flask import Blueprint, request, jsonify, current_app
from schema import SchemaError

from api.models import User
from api.modules.validators import (user_registration_validator,
                                    user_auth_validator)
from api.modules.user import registrate_user, authenticate


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
    """
    try:
        user_registration_validator.validate(request.json)
        user = registrate_user(request.json['username'],
                               request.json['email'],
                               request.json['password'])
        return jsonify(message='success', token=user.generate_token()), 201
    except SchemaError:
        return jsonify(message='invalid data'), 400


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
    try:
        user_auth_validator.validate(request.json)
        token = authenticate(request.json['username'],
                             request.json['password'])
        if token:
            return jsonify(message='success', token=token), 200
        return jsonify(message='invalid credentials'), 401
    except SchemaError:
        return jsonify(message='invalid data'), 400