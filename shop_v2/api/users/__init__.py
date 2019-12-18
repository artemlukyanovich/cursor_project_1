from flask import Blueprint
from flask_restful import Api
from app.users.resource import User

api_bp = Blueprint('users', __name__)
api = Api(api_bp)

api.add_resource(User, '/user')

