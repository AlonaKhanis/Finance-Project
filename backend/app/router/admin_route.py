from functools import wraps
from flask import current_app, jsonify, request
import jwt
from app.models import User

def role_required(roles):
    
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({"error": "Token is missing!"}), 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = User.query.get(data['user_id'])
                if not current_user:
                    return jsonify({"error": "User not found!"}), 404

                # Check if the current user's role is in the list of allowed roles
                if current_user.role not in roles and current_user.user_id != kwargs.get('user_id'):
                    return jsonify({"error": "Access denied."}), 403

            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token!"}), 401

            return f(current_user, *args, **kwargs)

        return decorated_function
    return decorator
