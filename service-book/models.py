from flask_sqlalchemy import SQLAlchemy
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Role(PyEnum):
    USER = 'USER'
    ADMIN = 'ADMIN'

class User(db.Model):
    __table_name__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(162), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    user_book = relationship("UserBook", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)


class Language(PyEnum):
    UKR = 'UKR'
    ENG = 'ENG'
    GER = 'GER'


class Book(db.Model):
    __table_name__ = "book"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    lang = db.Column(db.Enum(Language), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    cover = db.Column(db.String(200), nullable=False)
    user_book = relationship("UserBook", back_populates="book")


class UserBook(db.Model):
    __table_name__ = "user_book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, ForeignKey('book.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    user = relationship("User", back_populates="user_book")
    book = relationship("Book", back_populates="user_book")
