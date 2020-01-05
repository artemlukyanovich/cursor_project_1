from flask import Blueprint
from flask_restful import Api
from app.products.resource import AddProduct, ShowProducts, ShowProductDetails, ShoppingCart, AddToCart, Checkout, Clear

api_bp = Blueprint('products', __name__)
api = Api(api_bp)

api.add_resource(AddProduct, '/add_product')
api.add_resource(ShowProducts, '/products')
api.add_resource(ShowProductDetails, '/products/<int:id>')
api.add_resource(ShoppingCart, '/cart')
api.add_resource(AddToCart, '/cart/<int:id>')
api.add_resource(Checkout, '/checkout')
api.add_resource(Clear, '/clear')

