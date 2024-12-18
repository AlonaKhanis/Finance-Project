from flask import Blueprint
from app.router.admin_route import role_required


budget_bp = Blueprint('budgets' , __name__)


@budget_bp.route('/add_budget' , methods=['POST'])
@role_required('user')
def add_budget(current_user):
    pass


@budget_bp.route('/get_budget' , methods=['GET'])
@role_required('user')
def get_budget(current_user):
    pass

@budget_bp.route('/get_budget/<int:budget_id>' , methods=['GET'])
@role_required('user')
def get_budget_by_id(current_user , budget_id):
    pass

@budget_bp.route('/delete_budget/<int:budget_id>' , methods=['DELETE'])
@role_required('user')
def delete_budget(current_user , budget_id):
    pass

@budget_bp.route('/update_budget/<int:budget_id>' , methods=['PUT'])
@role_required('user')
def update_budget(current_user , budget_id):
    pass

