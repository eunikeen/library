import jwt
import datetime
from functools import wraps
from flask import request, jsonify

SECRET_KEY = "secret123"

def generate_token(user):
    payload = {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
        except:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated


def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user["role"] != "admin":
            return jsonify({"message": "Admin only"}), 403
        return f(*args, **kwargs)

    return decorated