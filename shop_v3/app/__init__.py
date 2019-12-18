from flask import Flask

from app.db import db, migrate, login
from config import Config, get_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.auth import api_bp as auth_bp


# def create_app(env="DEFAULT"):
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     db = SQLAlchemy(app)
#     migrate = Migrate(app, db)
#     login = LoginManager(app)
#     login.login_view = 'login'
#
#     app.register_blueprint(auth_bp)
#
#     with app.app_context():
#         db.create_all()
#
#     return app

def create_app(env="DEFAULT"):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    app.register_blueprint(auth_bp)

    db.init_app(app)
    login.init_app(app)
    db.drop_all(app=app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app


