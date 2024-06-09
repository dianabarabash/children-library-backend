from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import check_password_hash
from models import db, User
import redis
import uuid
from config import Config

r = redis.StrictRedis.from_url(Config.REDIS_URL)

class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            session_id = str(uuid.uuid4())
            r.set(session_id, user.id)
            return {'message': 'Authentication successful', 'session_id': session_id}, 200

        return {'message': 'Invalid credentials'}, 401
