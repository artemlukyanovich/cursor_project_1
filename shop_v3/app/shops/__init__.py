from flask import Blueprint
from flask_restful import Api
from app.shops.resource import AddShop, ProductToShop

api_bp = Blueprint('shops', __name__)
api = Api(api_bp)

api.add_resource(AddShop, '/add_shop')
api.add_resource(ProductToShop, '/product_to_shop')

