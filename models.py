from ext import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image = db.Column(db.String(255), default="default.jpg")

    comments = db.relationship("Comment", backref="product", lazy=True, cascade="all, delete-orphan")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), default="default.jpg")
    is_admin = db.Column(db.Boolean, default=False)

    comments = db.relationship("Comment", backref="author", lazy=True)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    text = db.Column(db.Text, nullable=False)

    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)