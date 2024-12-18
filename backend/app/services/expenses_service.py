from sqlalchemy.exc import SQLAlchemyError
from app.models import db, Category, Expense
import logging

logger = logging.getLogger(__name__)

def handle_db_error(operation, error):
    """Handles database errors and logs them consistently."""
    db.session.rollback()
    logger.error(f"Database error during {operation}: {error}")
    return {'error': 'Database error occurred. Please try again later.'}, 500

def handle_unexpected_error(operation, error):
    """Handles unexpected errors and logs them consistently."""
    db.session.rollback()
    logger.error(f"Unexpected error during {operation}: {error}")
    return {'error': 'An unexpected error occurred. Please try again later.'}, 500

def add_expense_service(data, current_user):
    try:
        amount = data.get('amount')
        category_id = data.get('category_id')
        description = data.get('description', '')
        is_recurring = data.get('is_recurring', False)

        if not amount or not category_id:
            return {"error": "Amount and category ID are required."}, 400
        if amount <= 0:
            return {"error": "Amount must be greater than zero."}, 400

        expense = Expense(
            user_id=current_user.user_id,
            category_id=category_id,
            price=amount,
            description=description,
            is_recurring=is_recurring,
        )
        db.session.add(expense)
        db.session.commit()

        logger.info(f"message : Expense added successfully , expense_id {expense.expense_id}")
                    
        return {"message": "Expense added successfully.", "expense_id": expense.expense_id}, 201

    except SQLAlchemyError as se:
        return handle_db_error("adding expense", se)
    except Exception as e:
        return handle_unexpected_error("adding expense", e)

def get_expenses_service(current_user):
    try:
        expenses = Expense.query.filter_by(user_id=current_user.user_id).all()
        expenses_list = [
            {
                'expense_id': expense.expense_id,
                'amount': expense.price,
                'description': expense.description,
                'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for expense in expenses
        ]

        return expenses_list, 200

    except SQLAlchemyError as se:
        return handle_db_error("retrieving expenses", se)
    except Exception as e:
        return handle_unexpected_error("retrieving expenses", e)

def get_expense_by_id_service(current_user, expense_id):
    try:
        expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
        if not expense:
            return {"error": "Expense not found."}, 404

        return {
            'expense_id': expense.expense_id,
            'amount': expense.price,
            'description': expense.description,
            'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }, 200

    except SQLAlchemyError as se:
        return handle_db_error("retrieving expense by ID", se)
    except Exception as e:
        return handle_unexpected_error("retrieving expense by ID", e)

def delete_expense_service(current_user, expense_id):
    try:
        expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
        if not expense:
            return {"error": "Expense not found."}, 404

        db.session.delete(expense)
        db.session.commit()
        logger.info(f"Expense ID:{expense_id} deleted successfully.")
        return {"message": "Expense deleted successfully."}, 200

    except SQLAlchemyError as se:
        return handle_db_error("deleting expense", se)
    except Exception as e:
        return handle_unexpected_error("deleting expense", e)

def update_expense_service(current_user, expense_id, data):
    try:
        amount = data.get('amount')
        category_id = data.get('category_id')
        description = data.get('description', '')
        is_recurring = data.get('is_recurring', False)

        if not amount or not category_id:
            return {"error": "Amount and category ID are required."}, 400
        if amount <= 0:
            return {"error": "Amount must be greater than zero."}, 400

        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            return {"error": "Invalid category ID."}, 400

        expense = Expense.query.filter_by(user_id=current_user.user_id, expense_id=expense_id).first()
        if not expense:
            return {"error": "Expense not found."}, 404

        expense.price = amount
        expense.category_id = category_id
        expense.description = description
        expense.is_recurring = is_recurring

        db.session.commit()
        return {"message": "Expense updated successfully."}, 200

    except SQLAlchemyError as se:
        return handle_db_error("updating expense", se)
    except Exception as e:
        return handle_unexpected_error("updating expense", e)

def get_expenses_by_category_service(current_user, category_id):
    try:
        expenses = Expense.query.filter_by(user_id=current_user.user_id, category_id=category_id).all()
        expenses_list = [
            {
                'expense_id': expense.expense_id,
                'amount': expense.price,
                'description': expense.description,
                'created_date': expense.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for expense in expenses
        ]

        logger.info("Expenses retrieved successfully by category.")
        return expenses_list, 200

    except SQLAlchemyError as se:
        return handle_db_error("retrieving expenses by category", se)
    except Exception as e:
        return handle_unexpected_error("retrieving expenses by category", e)
