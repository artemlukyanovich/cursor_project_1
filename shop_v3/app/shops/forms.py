from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NoneOf

from app.db import Shops, Products


class AddShopForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), NoneOf('All Shops', message='Incorrect name.')])
    city = StringField('City', validators=[DataRequired()])
    owner = StringField('Owner')
    submit = SubmitField('Add')


class ProductToShopForm(FlaskForm):
    shop = QuerySelectField('Shop', validators=[DataRequired()], query_factory=lambda: Shops.query.all())
    product = QuerySelectField('Product', validators=[DataRequired()], query_factory=lambda: Products.query.all())
    submit = SubmitField('Add')


