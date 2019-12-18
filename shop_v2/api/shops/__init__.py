from flask import Blueprint
from flask_restful import Api
from app.shops.resource import Shop

api_bp = Blueprint('shops', __name__)
api = Api(api_bp)

api.add_resource(Shop, '/shops')