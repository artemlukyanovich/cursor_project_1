import os
import sqlalchemy
from flask import render_template, flash, redirect, url_for, make_response, session, app
from flask_login import current_user
from flask_restful import Resource
from sqlalchemy import func
from werkzeug.utils import secure_filename
from app.db import db, headers, Products
from app.products.forms import AddProductForm, SearchForm, CartForm


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
        form = CartForm()
        return make_response(render_template("products/product_details.html", product=product,
                                             title=Products.query.get(id).name, form=form, fix=fix), 200, headers)

    def post(self, id):
        product = Products.query.get(id)
        form = CartForm()

        if form.validate_on_submit():
            # Checks to see if the user has already started a cart.
            if 'cart' in session:
                # If the product is not in the cart, then add it.
                print('1')
                print(session['cart'])
                if not any(product.name in d.keys() for d in session['cart']):
                    session['cart'].append({product.name: {'quantity': form.quantity.data, 'price': product.price,
                                                           'total': form.quantity.data * product.price}})
                    # return 'hi'
                    print('1.1')
                    print(session['cart'])

                # If the product is already in the cart, update the quantity
                elif any(product.name in d.keys() for d in session['cart']):
                    for d in session['cart']:
                        d.update((k, form.quantity.data) for k, v in d.items() if k == product.name)
                        print('1.2')

            else:
                # In this block, the user has not started a cart, so we start it for them and add the product.
                session['cart'] = [{product.name: form.quantity.data}]
                print('1.3')

            flash("Successfully added to cart.")
            return redirect("/cart")

        return make_response(render_template("products/product_details.html", product=product,
                                             title=Products.query.get(id).name, form=form), 200, headers)


class ShoppingCart(Resource):
    def get(self):
        ids_in_cart = session.get('cart', [])
        id2_count = len(ids_in_cart)
        return make_response(render_template("products/cart.html", id2=id2_count,
                                             title="Cart", products=session['cart'], fix=fix), 200, headers)


class AddToCart(Resource):
    def get(self, id):
        product = Products.query.get(id)

        if 'cart' in session:
            # If the product is not in the cart, then add it.
            if not any(product.name in d for d in session['cart']):
                session['cart'].append({product.name: cart.quantity.data})

            # If the product is already in the cart, update the quantity
            elif any(product.name in d for d in session['cart']):
                for d in session['cart']:
                    d.update((k, cart.quantity.data) for k, v in d.items() if k == product.name)

        else:
            # In this block, the user has not started a cart, so we start it for them and add the product.
            session['cart'] = [{product.name: cart.quantity.data}]

        return redirect("/cart")


class Checkout(Resource):
    def get(self):
        flash("Successfully paid.")
        return redirect("/products")


class Clear(Resource):
    def get(self):
        session['cart'].clear()
        flash("Successfully cleared.")
        return redirect("/products")
