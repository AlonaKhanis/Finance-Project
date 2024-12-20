from flask import Blueprint, jsonify, request
from app.router.admin_route import role_required
from app.services.budget_services import (
    add_budget_service,
    get_budget_service,
    get_budget_by_id_service,
    delete_budget_service,
    update_budget_service
)

budget_bp = Blueprint('budgets' , __name__)


@budget_bp.route('/add_budget' , methods=['POST'])
@role_required('user')
def add_budget(current_user):
    try:
        data = request.get_json(force=True) or {}
        response , status_code = add_budget_service(data , current_user)
        return jsonify(response) , status_code
    except Exception as e:
        return jsonify({'error' : 'An unexpected error occurred'}) , 500


@budget_bp.route('/get_budget' , methods=['GET'])
@role_required('user')
def get_budget(current_user):
    try:
        response , status_code = get_budget_service(current_user)
        return jsonify(response) , status_code
    except Exception as e:
        return jsonify({'error' : 'An unexpected error occurred'}) , 500

@budget_bp.route('/get_budget/<int:budget_id>' , methods=['GET'])
@role_required('user')
def get_budget_by_id(current_user , budget_id):
    try:
        response , status_code = get_budget_by_id_service(current_user , budget_id)
        return jsonify(response) , status_code
    except Exception as e:
        return jsonify({'error' : 'An unexpected error occurred'}) , 500
    

@budget_bp.route('/delete_budget/<int:budget_id>' , methods=['DELETE'])
@role_required('user')
def delete_budget(current_user , budget_id):
    try: 
        response , status_code = delete_budget_service(current_user , budget_id)
        return jsonify(response) , status_code
    except Exception as e:
        return jsonify({'error' : 'An unexpected error occurred'}) , 500
    

@budget_bp.route('/update_budget/<int:budget_id>' , methods=['PUT'])
@role_required('user')
def update_budget(current_user , budget_id):
    try:
        data = request.get_json(force=True) or {}
        response , status_code = update_budget_service(current_user , budget_id , data)
        return jsonify(response) , status_code
    except Exception as e:
        return jsonify({'error' : 'An unexpected error occurred'}) , 500

