# backend/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# Set up Flask-SQLAlchemy instance
db = SQLAlchemy()
Base = db.Model

# For compatibility with manual engine usage if needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False)

def init_db(app):
    """
    Bind the SQLAlchemy db instance to the Flask app and create tables.
    """
    db.init_app(app)

    with app.app_context():
        db.create_all()
