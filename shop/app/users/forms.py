# from flask_wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, BooleanField, Form, StringField, validators
from wtforms.validators import Required, EqualTo, Email


class LoginForm(Form):
    email = StringField('Email address', [[validators.DataRequired()], Email()])
    password = PasswordField('Password', [[validators.DataRequired()]])


class RegisterForm(Form):
    name = StringField('NickName', [[validators.DataRequired()]])
    email = StringField('Email address', [[validators.DataRequired()], Email()])
    password = PasswordField('Password', [[validators.DataRequired()]])
    confirm = PasswordField('Repeat Password', [
        [validators.DataRequired()],
        EqualTo('password', message='Passwords must match')
    ])
    accept_tos = BooleanField('I accept the TOS', [Required()])
    # recaptcha = RecaptchaField()

