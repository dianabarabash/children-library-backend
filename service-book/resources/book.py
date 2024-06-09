import datetime

from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db, Book, Language, UserBook
import redis
from config import Config

r = redis.StrictRedis.from_url(Config.REDIS_URL)

book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, help='Title is required')
book_parser.add_argument('lang', type=str, required=True, help='Language is required')
book_parser.add_argument('age', type=int, required=True, help='Age is required')
book_parser.add_argument('pages', type=int, required=True, help='Pages are required')
book_parser.add_argument('description', type=str, required=True, help='Description is required')
book_parser.add_argument('cover', type=str, required=True, help='Cover URL is required')


def _get_current_user_id():
    session_id = request.headers.get('Session-ID')
    user_id = int(r.get(session_id))
    return user_id


class BookResource(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return {
            'id': book.id,
            'title': book.title,
            'lang': book.lang.value,
            'age': book.age,
            'pages': book.pages,
            'description': book.description,
            'cover': book.cover
        }

    def post(self):
        args = book_parser.parse_args()
        book = Book(
            title=args['title'],
            lang=Language(args['lang']),
            age=args['age'],
            pages=args['pages'],
            description=args['description'],
            cover=args['cover']
        )
        db.session.add(book)
        db.session.commit()
        return {
            'id': book.id,
            'title': book.title,
            'lang': book.lang.value,
            'age': book.age,
            'pages': book.pages,
            'description': book.description,
            'cover': book.cover
        }, 201

    def delete(self, book_id):
        book = Book.query.filter_by(id=book_id).one_or_404()
        user_books = UserBook.query.filter_by(id=book_id).all()

        for user_book in user_books:
            db.session.delete(user_book)
        db.session.delete(book)
        db.session.commit()
        return '', 204


class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [
            {
                'id': book.id,
                'title': book.title,
                'lang': book.lang.value,
                'age': book.age,
                'pages': book.pages,
                'description': book.description,
                'cover': book.cover
            }
            for book in books
        ]


class UserBookResource(Resource):

    def get(self, book_id):
        user_id = _get_current_user_id()

        user_book = UserBook.query.filter_by(book_id=book_id, user_id=user_id).one_or_404()
        result = {
            'id': user_book.book_id,
            'start_date': str(user_book.start_date),
            'end_date': str(user_book.end_date)
        }

        return result, 200

    def put(self, book_id):
        user_id = _get_current_user_id()

        user_book = UserBook(book_id=book_id, user_id=user_id)
        db.session.add(user_book)
        db.session.commit()

        return {'message': 'Book created successfully', 'book_id': book_id}, 201

    def delete(self, book_id):
        user_id = _get_current_user_id()

        user_book = UserBook.query.filter_by(book_id=book_id, user_id=user_id).one_or_404()
        db.session.delete(user_book)
        db.session.commit()
        return "", 204


class UserBookStartReading(Resource):
    def post(self, book_id):
        user_id = _get_current_user_id()

        user_book_query = UserBook.query.filter_by(book_id=book_id, user_id=user_id)
        user_book = user_book_query.first()
        if not user_book:
            return {'message': 'Book is not in the reading list', 'book_id': book_id}, 400

        if user_book.end_date:
            return {'message': 'Book has been already read', 'book_id': book_id}, 400

        user_book_query.update({'end_date': datetime.datetime.now()})
        db.session.commit()
        return {'message': 'You have started reading the book', 'book_id': book_id}, 201


class UserBookStopReading(Resource):
    def post(self, book_id):
        user_id = _get_current_user_id()

        user_book_query = UserBook.query.filter_by(book_id=book_id, user_id=user_id)
        user_book = user_book_query.first()
        if not user_book:
            return {'message': 'Book is not in the reading list', 'book_id': book_id}, 400

        if not user_book.start_date:
            return {'message': 'You have not started reading the book', 'book_id': book_id}, 400

        user_book_query.update({'end_date': datetime.datetime.now()})
        db.session.commit()
        return {'message': 'You have finished reading the book', 'book_id': book_id}, 201
