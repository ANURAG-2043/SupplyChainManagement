
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

mock_user = {
    "email": "test@example.com",
    "password": "password123"
}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['email'] == mock_user['email'] and data['password'] == mock_user['password']:
        return jsonify(access_token='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'),200  # Replace with actual token generation logic
    return jsonify(msg="Bad email or password"), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify(message="Successfully logged out"), 200
