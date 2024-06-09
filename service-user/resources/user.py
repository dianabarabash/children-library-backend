from flask_restful import Resource, reqparse
from models import db, User, Role

user_parser = reqparse.RequestParser()
user_parser.add_argument('email', type=str, required=True, help='Email is required')
user_parser.add_argument('password', type=str, required=True, help='Password is required')


class UserResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        if User.query.filter_by(email=args['email']).first():
            return {'message': 'User already exists'}, 400

        user = User(email=args['email'], role=Role.USER)
        user.set_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully', 'user_id': user.id}, 201
