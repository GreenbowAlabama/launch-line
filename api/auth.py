import os
import psycopg2
from flask import Blueprint, request, jsonify
from passlib.hash import bcrypt
from api.jwt_utils import create_jwt, decode_jwt

auth_bp = Blueprint("auth", __name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "launch_lab"),
        user=os.getenv("DB_USER", "launch_admin"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432)
    )

@auth_bp.route("/register", methods=["POST"])
def register():
    allow_registration = os.getenv("ALLOW_REGISTRATION", "false").lower() == "true"
    if not allow_registration:
        return jsonify({"error": "Public registration is disabled"}), 403

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    hashed_pw = bcrypt.hash(password)
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
            (email, hashed_pw),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered"}), 201
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row or not bcrypt.verify(password, row[0]):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_jwt({"sub": email})
        return jsonify({"token": token})

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

@auth_bp.route("/me", methods=["GET"])
def me():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = decode_jwt(token)
        return jsonify({"email": payload["sub"]})
    except Exception:
        return jsonify({"error": "Invalid token"}), 401

@auth_bp.route("/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE email = %s", (email,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()

        if deleted == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"status": f"Deleted user {email}"}), 200

    except Exception as e:
        return jsonify({"error": f"Delete failed: {str(e)}"}), 500