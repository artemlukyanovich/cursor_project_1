from flask import session
from flask_wtf import FlaskForm
from sqlalchemy import func
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired

from app.db import category_list, Products


class AddProductForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()],
                      render_kw={"class": "form-control", "accept": "image/jpeg,image/png"})
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=category_list)
    definition = TextAreaField('Definition')
    price = IntegerField('Price')
    submit = SubmitField('Add')


class SearchForm(FlaskForm):
    name = StringField('Name')
    category = SelectField('Category', choices=[("%", "All Categories")]+category_list)
    price_from = StringField('Price')
    price_to = StringField('Price')
    submit = SubmitField('Filter')

