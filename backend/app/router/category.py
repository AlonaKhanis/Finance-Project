
from flask import Blueprint, jsonify, request
from app.router.admin_route import role_required
from app.services.category_services import get_all_categories , get_category_by_id_service , add_category ,update_category_service , delete_category_service

from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)
category_bp = Blueprint('category', __name__)



@category_bp.route('/get_categories', methods=['GET'])
@role_required(['user', 'admin'])
def get_categories(current_user):
                
        category_list , status_code = get_all_categories()
        
        if not category_list:
            logger.warning("No categories found.")
            return ({'error': 'No categories available'}), 404
        
        return jsonify(category_list), status_code



@category_bp.route('/get_category/<int:category_id>', methods=['GET'])
@role_required(['user', 'admin'])
def get_category_by_id(current_user, category_id):
    category_data, status_code = get_category_by_id_service(category_id)
    return jsonify(category_data), status_code



@category_bp.route('/add_category', methods=['POST'])
@role_required(['admin'])
def create_category(current_user):
    data = request.get_json()
    response, status_code = add_category(data)
    return jsonify(response), status_code

@category_bp.route('/update_category/<int:category_id>', methods=['PUT'])
@role_required('admin')
def update_category(current_user, category_id):
    data = request.get_json()
    response, status_code = update_category_service(category_id, data)
    return jsonify(response), status_code

@category_bp.route('/delete_category/<int:category_id>', methods=['DELETE'])
@role_required('admin')
def delete_category(current_user, category_id):
    response, status_code = delete_category_service(category_id)
    return jsonify(response), status_code


