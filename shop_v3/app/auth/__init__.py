from flask import Blueprint
from flask_restful import Api
from app.auth.resource import Index, Login, Logout, Register

api_bp = Blueprint('auth', __name__)
api = Api(api_bp)

api.add_resource(Index, '/', '/index')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/register')

