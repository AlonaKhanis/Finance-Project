from datetime import datetime
from flask import Blueprint, current_app, jsonify, request
from app.services.users_services import delete_user_service, get_all_users , get_user_by_id_service, update_user_service 
from .admin_route import role_required
from app.models import db

import logging

logger = logging.getLogger(__name__)

user_bp = Blueprint('users', __name__)



@user_bp.route('/get_all_users', methods=['GET'])
@role_required('admin') 
def get_users(_):
    try:
      
        users_list, status_code = get_all_users()
        return jsonify(users_list), status_code
    
    except Exception as e:
        logger.exception(f"Unexpected error in /get_users route: {e}")
        return jsonify({"error": "An unexpected error occurred."}), 500


@user_bp.route('/get_user_by_id/<int:user_id>', methods=['GET'])
@role_required('admin')
def get_user_by_id(_, user_id):

    response , status_code = get_user_by_id_service(user_id)
    return jsonify(response), status_code
    
    

@user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
@role_required(['admin' , 'user'])
def update_user(_,user_id):

    data = request.get_json()
    response , status_code = update_user_service(user_id, data)
    return jsonify(response), status_code
    


@user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@role_required('admin')
def delete_user(_, user_id):
    
    response , status_code = delete_user_service(user_id)
    return jsonify(response) , status_code



