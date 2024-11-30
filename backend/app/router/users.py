from datetime import datetime
from flask import Blueprint, current_app, jsonify, request
import jwt
import pytz
from app.models import User
from .admin_route import role_required
from app.models import db

user_bp = Blueprint('users', __name__)


def convert_to_local_time(utc_dt, tz_name=None):
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    if tz_name:
        local_tz = pytz.timezone(tz_name)
    else:
        local_tz = datetime.now().astimezone().tzinfo
    return utc_dt.astimezone(local_tz)

@user_bp.route('/get_users', methods=['GET'])
@role_required('admin')
def get_users(current_user): 
    users = User.query.all()
    users_list = []
    for user in users:
        local_created_date = convert_to_local_time(user.created_date)
        users_list.append({
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(users_list), 200

@user_bp.route('/get_user/<int:user_id>', methods=['GET'])
@role_required('admin')
def get_user_by_id(current_user, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found."}), 404
    local_created_date = convert_to_local_time(user.created_date)
    user_info = {
        'user_id': user.user_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return jsonify(user_info), 200

@user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@role_required('admin')
def update_user(current_user, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found."}), 404
    data = request.get_json()
    print(data)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({"message": "User updated successfully."}), 200

@user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(current_user, user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        return jsonify({"error": "User not found."}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."}), 200


@user_bp.route('/get_user_profile', methods=['GET'])
def get_user_profile():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return jsonify({"error": "Token is missing or malformed!"}), 401

    try:
        token = token.split(" ")[1]
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = User.query.get(data['user_id'])
        if not current_user:
            return jsonify({"error": "User not found!"}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401


    local_created_date = convert_to_local_time(current_user.created_date)
    user_profile = {
        'user_id': current_user.user_id,
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'email': current_user.email,
        'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_date': current_user.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
    }
    return jsonify(user_profile), 200

# @user_bp.route('/change_password', methods=['PUT'])
# def change_password(current_user):
#     data = request.get_json()
#     old_password = data.get('old_password')
#     new_password = data.get('new_password')
#     if not current_user.check_password(old_password):
#         return jsonify({"error": "Invalid password."}), 400
#     current_user.set_password(new_password)
#     db.session.commit()
#     return jsonify({"message": "Password changed successfully."}), 200



