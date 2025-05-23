from flask import Blueprint, request, jsonify
from passlib.hash import bcrypt
from api.jwt_utils import create_jwt, decode_jwt

auth_bp = Blueprint("auth", __name__)

# In-memory user store (replace with DB later)
users = {}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if email in users:
        return jsonify({"error": "User already exists"}), 400

    users[email] = bcrypt.hash(password)
    return jsonify({"message": "User registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user_hash = users.get(email)
    if not user_hash or not bcrypt.verify(password, user_hash):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt({"sub": email})
    return jsonify({"token": token})

@auth_bp.route("/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = decode_jwt(token)
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"email": payload["sub"]})

@auth_bp.route("/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    if email not in users:
        return jsonify({"error": "User not found"}), 404

    del users[email]
    return jsonify({"status": f"Deleted user {email}"}), 200