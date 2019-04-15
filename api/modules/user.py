"""Module for user interactions."""
from flask import current_app
from sqlalchemy.exc import IntegrityError

from api.models import User


def registrate_user(user):
    """
    Receive the user data and saves it on the database.

    Args:
        username str: unique username to be registered.
        email str: unique email to be registered.
        password: password to hash and save.

    Returns:
        on success: registered user object.
        on failure: None
    """
    user.hash_password()
    try:
        current_app.session.add(user)
        current_app.session.commit()
        return user
    except IntegrityError:
        current_app.session.rollback()


def authenticate(username, password):
    """
    Authenticates given credentials and returns it's token on success
    and None on failure.
    """
    usr = current_app.session.query(User).filter_by(username=username).first()
    if usr:
        return usr.authenticate(password)
