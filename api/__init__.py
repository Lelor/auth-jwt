from flask import Flask, request, jsonify
from flask_cors import CORS

from .blueprints.user import bp as user_bp
from .models import session, init_db
from .serializer.user import configure


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    app.session = session
    CORS(app)
    configure(app)
    init_db()
    return app
