import os
from datetime import datetime
from time import strftime

import sqlalchemy
from flask import render_template, flash, redirect, url_for, make_response, session, app
from flask_login import current_user
from flask_restful import Resource
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.db import db, headers, Products, Purchases
from app.products.forms import AddProductForm, SearchForm, ProductForm


def fix(num, digits=2):
    return f"{num:.{digits}f}"


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
            product = Products(name=form.name.data, category_name=form.category.data.name,
                               definition=form.definition.data,
                               price=round(form.price.data, 2), img_path=img_path)
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
                                             title='Products', form=form, fix=fix), 200, headers)

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
            products = Products.query.filter(func.lower(Products.name).like("%{}%".format(name.lower()))). \
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


class ShowProductDetails(Resource):
    def get(self, id):
        product = Products.query.get(id)
        form = ProductForm()
        return make_response(render_template("products/product_details.html", product=product,
                                             title=Products.query.get(id).name, form=form, fix=fix), 200, headers)

    def post(self, id):
        product = Products.query.get(id)
        form = ProductForm()

        if form.validate_on_submit():
            # Checks to see if the user has already started a cart.
            if 'cart' in session:
                # If the product is not in the cart, then add it.
                if not any(product.name in d.keys() for d in session['cart']):
                    session['cart'].append({product.name: {'q': form.quantity.data, 'p': product.price,
                                                           't': form.quantity.data*product.price}})

                # If the product is already in the cart, update the quantity
                elif any(product.name in p.keys() for p in session['cart']):
                    print(session['cart'])
                    for p in session['cart']:
                        if product.name in p.keys():
                            p[product.name]['q'] = form.quantity.data
                            p[product.name]['t'] = form.quantity.data*product.price
                    # d.update((k, form.quantity.data) for k, v in d.items() if k == product.name)

            else:
                # In this block, the user has not started a cart, so we start it for them and add the product.
                session['cart'] = [{product.name: {'q': form.quantity.data, 'p': product.price,
                                                   't': form.quantity.data * product.price}}]

            flash("Successfully added to cart.")
            return redirect("/cart")

        return make_response(render_template("products/product_details.html", product=product,
                                             title=Products.query.get(id).name, form=form), 200, headers)


def get_total(value):
    total = 0
    for p in value:
        for i, j in p.items():
            total += j['t']
    return total


class ShoppingCart(Resource):
    def get(self):
        cart_list = session['cart']
        total = get_total(cart_list)
        return make_response(render_template("products/cart.html",
                                             title="Cart", products=cart_list, total=total, fix=fix), 200, headers)


class Checkout(Resource):
    def get(self):
        total = 2
        user_id = current_user.id
        date = datetime.now()
        cart_list = (session['cart'])
        total = get_total(cart_list)
        cart_list = str(cart_list)  # use eval() to convert it back
        purchase = Purchases(user_id=user_id, date=date, cart_list=cart_list, total=total)
        db.session.add(purchase)
        db.session.commit()
        flash("Successfully paid.")
        session['cart'].clear()
        return redirect("/products")


class Clear(Resource):
    def get(self):
        session['cart'].clear()
        flash("Successfully cleared.")
        return redirect("/products")


class PurchaseHistory(Resource):
    def get(self):
        purchase_list = Purchases.query.filter(Purchases.user_id == current_user.id)
        # spent = db.session.query(func.sum(Purchases.total))
        spent = 0
        for p in purchase_list:
            spent += p.total
        return make_response(render_template("products/purchase_history.html",
                                             title="Purchase History", purchase_list=purchase_list, spent=spent,
                                             fix=fix, eval=eval, strftime=strftime), 200, headers)
