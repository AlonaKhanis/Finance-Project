from flask import Blueprint , current_app, jsonify, request
from app.models import Category, Expense
from .admin_route import role_required
from app.models import db


expense_bp = Blueprint('expenses', __name__)



@expense_bp.route('/add_expense', methods=['POST'])
@role_required('user')
def add_expense(current_user):
    data = request.get_json()

    amount = data.get('amount')
    category_id = data.get('category_id')
    description = data.get('description', '') 
    is_recurring = data.get('is_recurring', False) 

    if not amount or not category_id:
        return jsonify({"error": "Amount and category ID are required."}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero."}), 400


    expense = Expense(
        user_id=current_user.user_id,
        category_id=category_id,
        price=amount, 
        description=description,
        is_recurring=is_recurring,
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify({"message": "Expense added successfully.", "expense_id": expense.expense_id}), 201


@expense_bp.route('/get_expenses', methods=['GET'])
@role_required('user')
def get_expenses(current_user):
    expenses = Expense.query.filter_by(user_id=current_user.user_id).all()
    expenses_list = []
    for expense in expenses:
        expenses_list.append({
            'expense_id': expense.expense_id,
            'amount': expense.price,
            'description': expense.description,
            'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(expenses_list), 200

@expense_bp.route('/get_expense/<int:expense_id>', methods=['GET'])
@role_required('user')
def get_expense(current_user, expense_id):
    expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
    if not expense:
        return jsonify({"error": "Expense not found."}), 404
    return jsonify({
        'expense_id': expense.expense_id,
        'amount': expense.price,
        'description': expense.description,
        'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
    }), 200


@expense_bp.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
@role_required('user')
def delete_expense(current_user, expense_id):
    expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
    if not expense:
        return jsonify({"error": "Expense not found."}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully."}), 200


@expense_bp.route('/update_expense/<int:expense_id>', methods=['PUT'])
@role_required('user')
def update_expense(current_user, expense_id):
    data = request.get_json()
    amount = data.get('amount')
    category_id = data.get('category_id')
    description = data.get('description', '')
    is_recurring = data.get('is_recurring', False)

    # Input validation
    if not amount or not category_id:
        return jsonify({"error": "Amount and category ID are required."}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than zero."}), 400

    # Validate category
    category = Category.query.filter_by(category_id=category_id).first()
    if not category:
        return jsonify({"error": "Invalid category ID."}), 400

    # Find the expense
    expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
    if not expense:
        return jsonify({"error": "Expense not found."}), 404

    # Update the expense
    expense.price = amount
    expense.category_id = category_id
    expense.description = description
    expense.is_recurring = is_recurring

    try:
        db.session.commit()
        return jsonify({"message": "Expense updated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    

@expense_bp.route('/get_expenses_by_category/<int:category_id>', methods=['GET'])
@role_required('user')
def get_expenses_by_category(current_user, category_id):
    expenses = Expense.query.filter_by(user_id=current_user.user_id, category_id=category_id).all()
    expenses_list = []
    for expense in expenses:
        expenses_list.append({
            'expense_id': expense.expense_id,
            'amount': expense.price,
            'description': expense.description,
            'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(expenses_list), 200    

# move to category route
@expense_bp.route('/get_categories', methods=['GET'])
@role_required(['user','admin'])
def get_expense_categories(current_user):    
    categories = Category.query.all()
    categories_list = []
    for category in categories:
        categories_list.append({
            'category_id': category.category_id,
            'name': category.name,
            'description': category.description,
            'created_date': category.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(categories_list), 200