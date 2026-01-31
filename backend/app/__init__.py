from flask import Flask, jsonify, request
from flask_cors import CORS
from .services import jarvis_service


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register routes
    app.register_blueprint(jarvis_service.bp)

    return app