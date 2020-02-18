import os
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from web_app.models import db, User, Tweet, migrate
from web_app.routes import my_routes


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", default="OOPS")

def create_app():
    app = Flask(__name__)

    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///web_app_331.db"
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(my_routes)
    return app
