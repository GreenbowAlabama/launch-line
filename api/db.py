# api/db.py

# Replace with persistent store later
_users = {}

def create_user(email, hashed_password):
    _users[email] = {"email": email, "password": hashed_password}

def get_user_by_email(email):
    return _users.get(email)