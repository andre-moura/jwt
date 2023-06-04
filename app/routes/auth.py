from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from app.utils.jwt import generate_token, decode_token, token_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    # Get data from the request
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate input data
    if not username or not email or not password:
        return jsonify({'message': 'Invalid input data'}), 400

    # Check if the user already exists
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username already exists'}), 409

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'Email address already registered'}), 409

    # Create a new user
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    # Get data from the request
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate input data
    if not username or not password:
        return jsonify({'message': 'Invalid input data'}), 400

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Generate JWT token
    token = generate_token(user.id)

    return jsonify({'token': token})


@auth.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Protected endpoint accessed by user: {current_user.username}'}), 200