from flask import current_app

from api.models import User


def registrate_user(username, email, password):
    user = User(username,
                email,
                password)
    current_app.session.add(user)
    current_app.session.commit()
    return user


def authenticate(username, password):
    user = User.query.filter_by(username=username)
    return user.authenticate(password)
