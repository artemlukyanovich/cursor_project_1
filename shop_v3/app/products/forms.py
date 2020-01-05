from flask import session
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField, IntegerField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NoneOf

from app.db import Products, Shops, Categories


class AddProductForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()],
                      render_kw={"class": "form-control", "accept": "image/jpeg,image/png"})
    name = StringField('Name', validators=[DataRequired(), NoneOf('All Products', message='Incorrect name.')])
    # category = SelectField('Category', validators=[DataRequired()], choices=category_list)
    category = QuerySelectField('Category', query_factory=lambda: Categories.query.all())
    definition = TextAreaField('Definition')
    price = FloatField('Price')
    submit = SubmitField('Add')


class SearchForm(FlaskForm):
    name = StringField('Name')
    price_from = StringField('Price')
    price_to = StringField('Price')
    category = QuerySelectField('Category', query_factory=lambda: [Categories(name='All Categories')] +
                                                                  (Categories.query.all()))
    # shop = QuerySelectField('Shop', query_factory=lambda: Shops.query.all())
    shop = QuerySelectField('Shop', query_factory=lambda: [Shops(name='All Shops')] + (Shops.query.all()))
    submit = SubmitField('Filter')


class CartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

