from flask import Flask, request, jsonify

from .models import session


def create_app():
    app = Flask(__name__)
    app.session = session
