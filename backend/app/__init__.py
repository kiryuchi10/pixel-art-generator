from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    from .routes import main

    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    CORS(app)
    app.register_blueprint(main)
    return app
