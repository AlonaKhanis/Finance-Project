from flask import Blueprint, current_app, jsonify, request
from .admin_route import role_required
from app.services.expenses_service import (
    add_expense_service,
    get_expenses_service,
    get_expense_by_id_service,
    delete_expense_service,
    update_expense_service,
    get_expenses_by_category_service,
)

expense_bp = Blueprint('expenses', __name__)


@expense_bp.route('/add_expense', methods=['POST'])
@role_required('user')
def add_expense(current_user):
    try:
        data = request.get_json(force=True) or {}
        response, status_code = add_expense_service(data, current_user)
        return jsonify(response), status_code
    except Exception as e:
        current_app.logger.error(f"Error in add_expense: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@expense_bp.route('/get_expenses', methods=['GET'])
@role_required('user')
def get_expenses(current_user):
    try:
        expenses_list, status_code = get_expenses_service(current_user)
        return jsonify(expenses_list), status_code
    except Exception as e:
        current_app.logger.error(f"Error in get_expenses: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@expense_bp.route('/get_expense/<int:expense_id>', methods=['GET'])
@role_required('user')
def get_expense_by_id(current_user, expense_id):
    try:
        response, status_code = get_expense_by_id_service(current_user, expense_id)
        return jsonify(response), status_code
    except Exception as e:
        current_app.logger.error(f"Error in get_expense_by_id: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@expense_bp.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
@role_required('user')
def delete_expense(current_user, expense_id):
    try:
        response, status_code = delete_expense_service(current_user, expense_id)
        return jsonify(response), status_code
    except Exception as e:
        current_app.logger.error(f"Error in delete_expense: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@expense_bp.route('/update_expense/<int:expense_id>', methods=['PUT'])
@role_required('user')
def update_expense(current_user, expense_id):
    try:
        data = request.get_json(force=True) or {}
        response, status_code = update_expense_service(current_user, expense_id, data)
        return jsonify(response), status_code
    except Exception as e:
        current_app.logger.error(f"Error in update_expense: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500


@expense_bp.route('/get_expenses_by_category/<int:category_id>', methods=['GET'])
@role_required('user')
def get_expenses_by_category(current_user, category_id):
    try:
        response, status_code = get_expenses_by_category_service(current_user, category_id)
        return jsonify(response), status_code
    except Exception as e:
        current_app.logger.error(f"Error in get_expenses_by_category: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500
