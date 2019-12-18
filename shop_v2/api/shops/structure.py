from flask_restful import fields

shop_structure = {
    "id": fields.Integer,
    "name": fields.String,
    "city": fields.String,
    "owner": fields.String
}