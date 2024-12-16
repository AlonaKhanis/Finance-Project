from datetime import datetime
from flask import Blueprint, current_app, jsonify, request
from app.services.users_services import delete_User, get_User_profile, get_all_users , fetch_user_by_id, update_User 
from .admin_route import role_required
from app.models import db

user_bp = Blueprint('users', __name__)


@user_bp.route('/get_all_users', methods=['GET'])
@role_required('admin') 
def get_users(_):
    try:
        users_list = get_all_users()
        
        if not users_list:
            return jsonify({"message": "No users found or an error occurred."}), 404
        
        return jsonify(users_list), 200
    
    except Exception as e:
        print(f"Error in /get_users route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500

@user_bp.route('/get_user_by_id/<int:user_id>', methods=['GET'])
@role_required('admin')
def get_user_by_id(_, user_id):
    try:
        user = fetch_user_by_id(user_id)

        if user is None:
            return jsonify({"error": "User not found."}), 404

        return jsonify(user), 200
    except Exception as e:
        print(f"Error in /get_user_by_id route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500
    

@user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@role_required(['admin' , 'user'])
def update_user(current_user, user_id):
    try:
        data = request.get_json()
        update_User(user_id, data, db)

        return jsonify({"message": "User updated successfully."}), 200
    
    except Exception as e:
        print(f"Error in /update_user route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500



@user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(_, user_id):
    
    try:
        delete_User(user_id, db)
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as e:
        print(f"Error in /delete_user route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@user_bp.route('/get_user_profile', methods=['GET'])
@role_required(['admin', 'user'])
def get_user_profile(current_user):

    try:
        user_profile = get_User_profile(current_user)

        return jsonify(user_profile), 200
    
    except Exception as e:
        print(f"Error in /get_user_profile route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500



