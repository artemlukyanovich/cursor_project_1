from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
headers = {'Content-Type': 'text/html; charset=utf-8'}


shops_products = db.Table(
    'shops_products',
    db.Column('shop_id', db.Integer, db.ForeignKey('shops.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'))
)


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    position = db.Column(db.String(64), default="user")
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


class Shops(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    owner = db.Column(db.String(64), index=True)
    products = db.relationship('Products', secondary=shops_products, backref='shops')

    def __repr__(self):
        # return '<Shop {}>'.format(self.name)
        return self.name


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64), index=True)
    definition = db.Column(db.String(256))
    price = db.Column(db.Integer, index=True)
    img_path = db.Column(db.String(256))
    # shops

    def __repr__(self):
        return self.name


category_list = [('for_men', 'For Men'), ('for_women', 'For Women')]

user_1 = Users(username='admin', email='admin@shop.com',
              password_hash=generate_password_hash('password'), position='admin')
user_2 = Users(username='user', email='user@shop.com',
              password_hash=generate_password_hash('password'))

shop_1 = Shops(name="Shop 1", city="Kiev", owner="Artem")
shop_2 = Shops(name="Shop 2", city="Lviv", owner="Ivan")

product_1 = Products(name="Cocosas", category='for_men', definition='Just coconuts', price=15,
                     img_path='app/static/products/default1.jpg')
product_2 = Products(name="Apelsinas", category='for_women', definition='Just oranges', price=5,
                     img_path='app/static/products/default2.jpg')