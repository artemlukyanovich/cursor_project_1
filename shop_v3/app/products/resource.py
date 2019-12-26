import os
import sqlalchemy
from flask import render_template, flash, redirect, url_for, make_response
from flask_login import current_user
from flask_restful import Resource
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.db import db, headers, Products
from app.products.forms import AddProductForm, SearchForm


class AddProduct(Resource):
    def get(self):
        if current_user.position != 'admin':
            return redirect(url_for('auth.index'))
        form = AddProductForm()
        return make_response(render_template('products/add_product.html', title='Add Product', form=form), 200, headers)

    def post(self):
        if current_user.position != 'admin':
            return redirect(url_for('auth.index'))
        form = AddProductForm()
        if form.validate_on_submit():
            image = form.image.data
            img_name = secure_filename(image.filename)
            img_path = os.path.join('app/static/products', img_name)
            image.save(img_path)
            product = Products(name=form.name.data, category_name=form.category.data, definition=form.definition.data,
                               price=form.price.data, img_path=img_path)
            db.session.add(product)
            db.session.commit()
            flash('Congratulations, the product was added!')
            return redirect(url_for('products.addproduct'))
        return make_response(render_template('products/add_product.html', title='Add Product', form=form), 200, headers)


class ShowProducts(Resource):
    def get(self):
        form = SearchForm()
        products = Products.query.order_by(Products.name)
        return make_response(render_template("products/products.html", products=products,
                                             title='Products', form=form), 200, headers)

    def post(self):
        form = SearchForm()
        products = Products.query.all()
        if form.validate_on_submit():
            name = form.name.data
            category = form.category.data
            shops = form.shop.data
            price_from = form.price_from.data
            if not price_from.isdigit():
                price_from = 0
            price_to = form.price_to.data
            if not price_to.isdigit():
                price_to = Products.query.order_by(sqlalchemy.desc(Products.price)).first().price
            products = Products.query.filter(func.lower(Products.name).like("%{}%".format(name.lower()))).\
                filter(Products.price.between(price_from, price_to))
            if category.name != "All Categories":
                products = products.filter(Products.category_name == category.name)
            if shops.name != "All Shops":
                products = products.filter(Products.shops.contains(form.shop.data))
            print(type(form.shop.data))
            return make_response(render_template("products/products.html", products=products,
                                                 title='Products', form=form), 200, headers)
        print(form.errors)
        return make_response(render_template("products/products.html", products=products,
                                             title='Products', form=form), 200, headers)

