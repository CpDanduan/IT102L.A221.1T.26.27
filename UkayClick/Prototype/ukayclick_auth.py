import hashlib
from ukayclick_storage import load_users, save_users

def _hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def login(username, password):
    username = username.strip()
    password_hash = _hash(password)
    for user in load_users():
        if user["username"] == username and user["password_hash"] == password_hash:
            return user
    return None

def register(username, password, confirm):
    username = username.strip()
    if not username or not password:
        return False, "Username and password are required."
    if password != confirm:
        return False, "Passwords do not match."
    users = load_users()
    if any(u["username"].lower() == username.lower() for u in users):
        return False, "Username already exists."
    users.append({"username": username, "password_hash": _hash(password)})
    save_users(users)
    return True, "Account created successfully."
