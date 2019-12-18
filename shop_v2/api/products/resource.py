import json
from flask import request
from flask_restful import Resource, marshal_with

from app.shops.structure import shop_structure
from app.db import db, Products


class Product(Resource):
    def get(self):
        @marshal_with(shop_structure)
        def show(x):
            return x
        return show(Products.query.all())

    def post(self):
        data = json.loads(request.data)
        new_prod = Products(**data)
        db.session.add(new_prod)
        db.session.commit()
        return "Successfully added!"

