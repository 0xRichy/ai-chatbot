from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

users = {}  # Simule une base de données d'utilisateurs

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    hashed_password = generate_password_hash(password, method='sha256')
    users[username] = hashed_password
    return jsonify({"message": "User registered"}), 201
