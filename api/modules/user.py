from flask import current_app
from sqlalchemy.exc import IntegrityError

from api.models import User


def registrate_user(username, email, password):
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
    user = User(username,
                email,
                password)
    try:
        current_app.session.add(user)
        current_app.session.commit()
        return user
    except IntegrityError:
        current_app.session.rollback()


def authenticate(username, password):
    usr = current_app.session.query(User).filter_by(username=username).first()
    if usr:
        return usr.authenticate(password)
