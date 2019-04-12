"""Module of schema validators to be used on the routes."""
from functools import wraps

from flask import request, abort, jsonify
from jwt import decode
from jwt.exceptions import (ExpiredSignatureError,
                            InvalidSignatureError,
                            DecodeError)
from schema import Schema

from api.models import secret


def validate_token(func):
    """
    Route decorator to validate that the token is present and is valid.

    If the token is successfully validated, the operation procceeds normally.
    If the token is expied or invalid, the message returned reflects that.

    In all cases where the token doesn't work, aborts with a status of 403
    (PERMISSION DENIED).
    """
    @wraps(func)
    def _inner(*args, **kwargs):
        token = request.headers.get('auth-token')
        if token:
            token = token.encode('utf-8')
            try:
                decode(token, secret, algorithms=['HS256'])
                return func(*args, **kwargs)
            except ExpiredSignatureError:
                abort(403, jsonify(message='expired token'))
            except (InvalidSignatureError, DecodeError):
                abort(403, jsonify(message='invalid token'))
        abort(403, jsonify(message='permission denied'))
    return _inner


user_registration_validator = Schema({'username': str,
                                      'email': str,
                                      'password': str})
user_auth_validator = Schema({'username': str,
                              'password': str})
