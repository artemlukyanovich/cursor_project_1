from flask_restful import fields

shop_structure = {
    "id": fields.Integer,
    "name": fields.String,
    "category": fields.String,
    "shop": fields.String,
    "description": fields.String
}