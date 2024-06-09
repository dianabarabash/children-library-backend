from flask import Blueprint
from flask_restful import Api
from .book import BookResource, BookListResource, UserBookResource, UserBookStartReading, UserBookStopReading

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(BookListResource, '/books')
api.add_resource(UserBookStartReading, '/book/<int:book_id>/user/start')
api.add_resource(UserBookStopReading, '/book/<int:book_id>/user/end')
api.add_resource(UserBookResource, '/book/<int:book_id>/user')
api.add_resource(BookResource, '/book', '/book/<int:book_id>')
