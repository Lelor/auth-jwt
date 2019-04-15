from flask import Flask, request, jsonify

from .blueprints.user import bp as user_bp
from .models import session
from .serializer.user import configure


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.session = session
    configure(app)
    return app
