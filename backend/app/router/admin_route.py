from functools import wraps
from flask import current_app, jsonify, request
import jwt
from app.models import User
import logging

logger = logging.getLogger(__name__)

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
                logger.warning("Token is missing in the request headers.")
                return jsonify({"error": "Token is missing!"}), 401

            try:
                data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
                user_id = data.get('user_id')

                if not user_id:
                    logger.warning("User ID not found in token!")
                    return jsonify({"error": "User ID not found in token!"}), 400

                current_user = User.query.get(user_id)
                if not current_user:
                    logger.warning("User not found!")
                    return jsonify({"error": "User not found!"}), 404

                # Check if the current user's role is in the list of allowed roles
                if current_user.role not in roles and current_user.user_id != kwargs.get('user_id'):
                    logger.error("Access denied.")
                    return jsonify({"error": "Access denied."}), 403

            except jwt.ExpiredSignatureError:
                logger.error("Token has expired!")
                return jsonify({"error": "Token has expired!"}), 401
            except jwt.InvalidTokenError:
                logger.error("Invalid token!")
                return jsonify({"error": "Invalid token!"}), 401

            return f(current_user, *args, **kwargs)

        return decorated_function
    return decorator
