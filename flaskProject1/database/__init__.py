""""
__init__.py
"""
import logging

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from database.config import Config

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.setLevel(logging.DEBUG)
    db.init_app(app)
    return app