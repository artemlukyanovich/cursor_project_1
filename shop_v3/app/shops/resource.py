from flask import render_template, flash, redirect, url_for, make_response
from flask_login import current_user
from flask_restful import Resource
from app.db import db, headers, Shops
from app.shops.forms import AddShopForm, ProductToShopForm


class AddShop(Resource):
    def get(self):
        if current_user.position != 'admin':
            return redirect(url_for('auth.index'))
        form = AddShopForm()
        return make_response(render_template('shops/add_shop.html', title='Add Shop', form=form), 200, headers)

    def post(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = AddShopForm()
        if form.validate_on_submit():
            shop = Shops(name=form.name.data, city=form.city.data, owner=form.owner.data)
            db.session.add(shop)
            db.session.commit()
            flash('Congratulations, the shop was added!')
            return redirect(url_for('shops.addshop'))
        return make_response(render_template('shops/add_shop.html', title='Add Shop', form=form), 200, headers)


class ProductToShop(Resource):
    def get(self):
        if current_user.position != 'admin':
            return redirect(url_for('auth.index'))
        form = ProductToShopForm()
        return make_response(render_template('shops/product_to_shop.html', title='Add Product to Shop', form=form),
                             200, headers)

    def post(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.index'))
        form = ProductToShopForm()
        if form.validate_on_submit():
            shop = form.shop.data
            product = form.product.data
            shop.products.append(product)
            db.session.commit()
            flash('Congratulations, the product was added to the shop!')
            return redirect(url_for('shops.producttoshop'))
        return make_response(render_template('shops/product_to_shop.html', title='Add Product to Shop', form=form),
                             200, headers)
