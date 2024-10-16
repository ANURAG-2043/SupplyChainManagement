from flask import Blueprint, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_jwt_extended import  create_refresh_token, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import logging

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

logging.basicConfig(level=logging.DEBUG)


def create_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# User registration route
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not email or not password or not confirm_password:
        return jsonify({"msg":"Missing required fields"}), 400
    
    if password != confirm_password:
        return jsonify({"msg":"Password do not match"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
# db
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"msg": "Email already registered"}), 400
    conn.close()

    return jsonify({"msg": "User registered successfully"}), 201

# login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    if not email or not password:
        return jsonify({"msg":"Missing email or password"}), 400
    
    # Fetch user from database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"msg": "Logout successful"}), 200

# logged in page
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    app.logger.info(f'User: {current_user}')
    return render_template('protected.html', user=current_user)

