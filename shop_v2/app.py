# from app.rooms import api_bp as rooms_bp
# from app.staff import api_bp as staff_bp
# from app.tenants import api_bp as tenants_bp

from flask import Flask
from config import get_config
from api.db import db, migrate


def create_app(env="DEFAULT"):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    # app.register_blueprint(rooms_bp)
    # app.register_blueprint(staff_bp)
    # app.register_blueprint(tenants_bp)

    db.init_app(app)
    db.drop_all(app=app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        """Some default data"""

        db.session.commit()

    return app

