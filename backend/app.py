from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from flask_mysqldb import MySQL
from models import mysql, User, SecurityTransaction
from config import Config

app = Flask(__name__)
app.config.from_object('config.Config')

mysql.init_app(app)
jwt = JWTManager(app)
CORS(app)

# @app._got_first_request
def create_default_admin():
    cur = mysql.connection.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE,
            password VARCHAR(200),
            address VARCHAR(200),
            contact_number VARCHAR(15),
            role VARCHAR(50) DEFAULT 'user'
        )
    ''')
    mysql.connection.commit()
    cur.close()
    User.create_user('Admin', 'admin@kic.com', 'kic_admin12', 'address', '9874563210', role='admin')  # Create default admin user


@app.route('/api/register', methods=['POST'])
def register():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    address = request.json.get('address')
    contact_number = request.json.get('contactNumber')

    if not name or not email or not password:
        return jsonify(message='Name, email, and password are required'), 400

    if User.get_user_by_email(email):
        return jsonify(message='Email already registered'), 409

    User.create_user(name, email, password, address, contact_number)
    return jsonify(message='User registered successfully'), 201


@app.route('/api/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.get_user_by_email(email)
    if not user:
        return jsonify(message='Bad email or password'), 401
    if not User.check_password(user, password):
        return jsonify(message='Bad email or password'), 401
    access_token = create_access_token(identity={'id': user[0], "email": user[2], 'role': user[6]})  # user[0] is ID, user[6] is role
    # return jsonify(token=access_token), 200
    return jsonify({"token": access_token, "user": {"email": user[2], "role": user[6]}}), 200


@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        users = User.get_all_users()
    else:
        users = [User.get_user_by_id(current_user['id'])]  # Get only the current user's data

    return jsonify([{
        'id': user[0],
        'name': user[1],
        'email': user[2],
        'address': user[4],
        'contactNumber': user[5],
        'role': user[6],
    } for user in users]), 200


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    print(current_user)
    user = User.get_user_by_email(current_user['email'])
    if not user:
        return jsonify(message='User not found'), 404

    if current_user['role'] != 'admin' and current_user['id'] != user_id:
        return jsonify(message='Permission denied'), 403

    name = request.json.get('name')
    # email = current_user['email']
    address = request.json.get('address')
    contact_number = request.json.get('contactNumber')

    if not name:
        return jsonify(message='Name is required'), 400

    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name = %s, address = %s, contact_number = %s WHERE id = %s",
                (name, address, contact_number, user_id))
    mysql.connection.commit()
    cur.close()
    return jsonify(message='User updated successfully'), 200


@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if current_user['role'] != 'admin':
        return jsonify(message='Permission denied'), 403

    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    address = request.json.get('address')
    contact_number = request.json.get('contactNumber')
    role = request.json.get('role', 'user')

    if not name or not email or not password:
        return jsonify(message='Name, email, and password are required'), 400

    if User.get_user_by_email(email):
        return jsonify(message='Email already registered'), 409

    User.create_user(name, email, password, address, contact_number, role)
    return jsonify(message='User created successfully'), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    user = User.get_user_by_id(current_user['id'])
    if not user:
        return jsonify(message='User not found'), 404
    if current_user['role'] != 'admin' and current_user['id'] != user_id:
        return jsonify(message='Permission denied'), 403
    User.delete_user(user_id)
    return jsonify(message='User deleted'), 200


@app.route('/api/combined-transactions', methods=['GET'])
# @jwt_required()
def get_combined_transactions():
    # page = int(request.args.get('page', 1))
    # per_page = int(request.args.get('per_page', 100))
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    portfolio_number = request.args.get('portfolio_number')
    share_symbol = request.args.get('share_symbol')
    security_currency = request.args.get('security_currency')

    # transactions, total = SecurityTransaction.get_combined_transactions(page, per_page, from_date, to_date, portfolio_number, share_symbol, security_currency)
    transactions, total = SecurityTransaction.get_combined_transactions(from_date, to_date, portfolio_number, share_symbol, security_currency)

    return jsonify({
        'records': [{
            'TRADE_DATE': transaction[0],
            'SECURITY_ACCOUNT': transaction[1],
            'SAM_NAME': transaction[2],
            'SECURITY_NUMBER': transaction[3],
            'SECURITY_NAME': transaction[4],
            'TRANS_TYPE': transaction[5],
            'RECID': transaction[6],
            'NO_NOMINAL': transaction[7],
            'PRICE': transaction[8],
            'NET_AMT_TRADE': transaction[9],
            'BROKER_COMMS': transaction[10],
            'PROF_LOSS_SEC_CCY': transaction[11]
        } for transaction in transactions],
        'totalRecords': total
    }), 200


if __name__ == '__main__':
    with app.app_context():
        create_default_admin()  # Create default admin user
    app.run(debug=True, port=8001)
    # app.run(host='0.0.0.0', port=80)
