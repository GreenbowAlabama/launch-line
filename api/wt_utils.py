# api/jwt_utils.py

import jwt
import datetime

SECRET = "dev-secret" 

def create_jwt(payload):
    return jwt.encode(
        {**payload, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)},
        SECRET,
        algorithm="HS256"
    )

def decode_jwt(token):
    return jwt.decode(token, SECRET, algorithms=["HS256"])