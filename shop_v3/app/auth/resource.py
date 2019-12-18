from flask import render_template, flash, redirect, url_for, request, make_response
from werkzeug.urls import url_parse

# from app import app, db
from app.auth.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.db import Users, db, headers

import json
from flask_restful import Resource, fields, marshal_with, reqparse


# @app.route('/')
# @app.route('/index')
# @login_required
class Index(Resource):
    def get(self):
        posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            },
            {
                'author': {'username': 'Ипполит'},
                'body': 'Какая гадость эта ваша заливная рыба!!'
            }
        ]
        # headers = {'Content-Type': 'text/html; charset=utf-8'}
        return make_response(render_template('auth/index.html', title='Home', posts=posts), 200, headers)


# @app.route('/login', methods=['GET', 'POST'])
class Login(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('auth.index')
            return redirect(next_page)
        # headers = {'Content-Type': 'text/html; charset=utf-8'}
        # return render_template('login.html', title='Sign In', form=form)
        return make_response(render_template('auth/login.html', title='Sign In', form=form), 200, headers)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('auth.index')
            return redirect(next_page)
        # headers = {'Content-Type': 'text/html; charset=utf-8'}
        # return render_template('login.html', title='Sign In', form=form)
        return make_response(render_template('auth/login.html', title='Sign In', form=form), 200, headers)


# @app.route('/logout')
class Logout(Resource):
    def get(self):
        logout_user()
        return redirect(url_for('auth.index'))


# @app.route('/register', methods=['GET', 'POST'])
class Register(Resource):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        return make_response(render_template('auth/register.html', title='Register', form=form), 200, headers)

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = Users(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('auth.login'))
        return make_response(render_template('auth/register.html', title='Register', form=form), 200, headers)

