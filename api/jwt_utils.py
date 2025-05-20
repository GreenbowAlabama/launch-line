# api/jwt_utils.py
import jwt
import datetime
from flask import current_app

def create_jwt(payload, expires_in_minutes=60):
    payload_copy = payload.copy()
    payload_copy['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_in_minutes)
    return jwt.encode(payload_copy, current_app.config['JWT_SECRET'], algorithm='HS256')

def decode_jwt(token):
    return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])