import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User
from datetime import datetime, timedelta

def generate_token(user_id):
    now = datetime.utcnow()
    expiration = now + current_app.config['TOKEN_EXPIRATION']
    token_payload = {'user_id': user_id, 'exp': expiration}
    token = jwt.encode(token_payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        decoded_token = decode_token(token)

        if not decoded_token:
            return jsonify({'message': 'Token is invalid or expired'}), 401

        user_id = decoded_token['user_id']
        current_user = User.query.get(user_id)

        if not current_user:
            return jsonify({'message': 'User not found'}), 404

        return func(current_user, *args, **kwargs)

    return decorated