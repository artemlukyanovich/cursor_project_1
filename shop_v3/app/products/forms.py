from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FileField
from wtforms.validators import DataRequired

from app.db import category_list


class AddProductForm(FlaskForm):
    image = FileField('Image', validators=[DataRequired()],
                      render_kw={"class": "form-control", "accept": "image/jpeg,image/png"})
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=category_list)
    definition = TextAreaField('Definition')
    submit = SubmitField('Add')

