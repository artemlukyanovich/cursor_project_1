from flask import Blueprint
from flask_restful import Api
from app.products.resource import AddProduct, ShowProducts

api_bp = Blueprint('products', __name__)
api = Api(api_bp)

api.add_resource(AddProduct, '/add_product')
api.add_resource(ShowProducts, '/products')

