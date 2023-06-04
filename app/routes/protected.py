from flask import Blueprint, jsonify
from app.utils.jwt import token_required
from app.models import User


protected = Blueprint('protected', __name__)

@protected.route('/greetings', methods=['GET'])
@token_required
def protected_endpoint(current_user):
    return jsonify({'message': f'Welcome! This is a protected endpoint for user {current_user.username}.'}), 200