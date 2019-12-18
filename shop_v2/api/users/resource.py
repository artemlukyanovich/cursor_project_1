import json
from flask import request
from flask_restful import Resource, marshal_with

from app.users.structure import user_structure
from app.db import db, Users


class User(Resource):
    def get(self):
        @marshal_with(user_structure)
        def show(x):
            return x
        return show(Users.query.all())

    def post(self):
        data = json.loads(request.data)
        new_user = Users(**data)
        db.session.add(new_user)
        db.session.commit()
        return "Successfully added!"

