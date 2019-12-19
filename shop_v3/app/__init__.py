from flask import Flask
from app.db import db, migrate, login, user_1, user_2, shop_1, shop_2, product_1, product_2
from config import Config, get_config
from app.auth import api_bp as auth_bp
from app.shops import api_bp as shops_bp
from app.products import api_bp as products_bp


def create_app(env="DEFAULT"):
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    app.register_blueprint(auth_bp)
    app.register_blueprint(shops_bp)
    app.register_blueprint(products_bp)

    db.init_app(app)
    login.init_app(app)
    db.drop_all(app=app)

    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        """Some default data"""
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(shop_1)
        db.session.add(shop_2)
        db.session.add(product_1)
        db.session.add(product_2)
        shop_1.products.append(product_2)
        db.session.commit()

    return app


