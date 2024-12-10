from flask import Flask
from .db import create_db_if_not_exists
from .routes import main

import secrets
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(32)
    app.config['DB_HOST'] = os.getenv('DB_HOST')
    app.config['DB_USER'] = os.getenv('DB_USER')
    app.config['DB_PASSWORD'] = os.getenv('DB_PASSWORD')
    app.config['DB_NAME'] = os.getenv('DB_NAME')

    with app.app_context():
        create_db_if_not_exists()

    app.register_blueprint(main)
    
    return app
