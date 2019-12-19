import os
from flask import render_template, flash, redirect, url_for, make_response
from flask_login import current_user
from flask_restful import Resource
from werkzeug.utils import secure_filename
from app.db import db, headers, Products
from app.products.forms import AddProductForm


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
            product = Products(name=form.name.data, category=form.category.data,
                               definition=form.definition.data, img_path=img_path)
            db.session.add(product)
            db.session.commit()
            flash('Congratulations, the product was added!')
            return redirect(url_for('products.addproduct'))
        return make_response(render_template('products/add_product.html', title='Add Product', form=form), 200, headers)

