
from flask import current_app
from app.models import Budget , db
from sqlalchemy.exc import SQLAlchemyError
from app.error_handlers import handle_db_error , handle_unexpected_error

def add_budget_service(data , current_user):
    try:
        new_budget = Budget(
            user_id = current_user.user_id,
            catgory_id = data.get('category_id'),
            amount = data.get('amount'),
            start_date = data.get('start_date'),
            end_date = data.get('end_date'),
        )

        current_app.logger.info("Budget added successfully")
        db.session.add(new_budget)
        db.session.commit()

        return {"message" : "Budget added successfully" , "budget_id" : new_budget.budget_id} , 201
    
    except SQLAlchemyError as se:
        return handle_db_error("adding budget" , se)
    except Exception as e:
        return handle_unexpected_error("adding budget" , e)
    
def get_budget_service(current_user):
    try:
        budgets = Budget.query.filter_by(user_id = current_user.user_id).all()
        budget_list = [
            {
                'budget_id' : budget.budget_id,
                'amount' : budget.amount,
                'start_date' : budget.start_date.strftime('%Y-%m-%d'),
                'end_date' : budget.end_date.strftime('%Y-%m-%d'),
            }
            for budget in budgets
        ]
        current_app.logger.info("Budget fetch successfuly")
        return budget_list , 200
    
    except SQLAlchemyError as se:
        return handle_db_error("retrieving budgets" , se)
    except Exception as e:
        return handle_unexpected_error("retrieving budgets" , e)
    

def get_budget_by_id_service(current_user , budget_id):
    try:
        budget = Budget.query.filter_by(user_id = current_user.user_id , budget_id = budget_id).first()
        if not budget:
            return {"error" : "Budget not found"} , 404

        return { "budget_id" : budget.budget_id , "amount" : budget.amount , "start_date" : budget.start_date.strftime('%Y-%m-%d') , "end_date" : budget.end_date.strftime('%Y-%m-%d')} , 200
    
    except SQLAlchemyError as se:
        return handle_db_error("retrieving budget by ID" , se)
    except Exception as e:
        return handle_unexpected_error("retrieving budget by ID" , e)
    
def delete_budget_service(current_user , budget_id):
    try:
        budget = Budget.query.filter_by(user_id = current_user.user_id , budget_id = budget_id).first()
        if not budget:
            return {"error" : "Budget not found"} , 404
        
        db.session.delete(budget)
        db.session.commit()
        current_app.logger.info("Budget deleted successfully")
        return {"message" : "Budget deleted successfully"} , 200
    
    except SQLAlchemyError as se:
        return handle_db_error("deleting budget" , se)
    except Exception as e:
        return handle_unexpected_error("deleting budget" , e)
    
def update_budget_service(current_user , budget_id , data):
    try:
        budget = Budget.query.filter_by(user_id = current_user.user_id , budget_id = budget_id).first()
        if not budget:
            return {"error" : "Budget not found"} , 404
        
        budget.amount = data.get('amount')
        budget.start_date = data.get('start_date')
        budget.end_date = data.get('end_date')
        db.session.commit()
        current_app.logger.info("Budget updated successfully")
        return {"message" : "Budget updated successfully"} , 200
    
    except SQLAlchemyError as se:
        return handle_db_error("updating budget" , se)
    except Exception as e:
        return handle_unexpected_error("updating budget" , e)
    
def get_budgets_by_category_service(current_user , category_id):
    try:
        budgets = Budget.query.filter_by(user_id = current_user.user_id , category_id = category_id).all()
        budget_list = [
            {
                'budget_id' : budget.budget_id,
                'amount' : budget.amount,
                'start_date' : budget.start_date.strftime('%Y-%m-%d'),
                'end_date' : budget.end_date.strftime('%Y-%m-%d'),
            }
            for budget in budgets
        ]
        current_app.logger.info("Budget fetch successfuly")
        return budget_list , 200
    
    except SQLAlchemyError as se:
        return handle_db_error("retrieving budgets by category" , se)
    except Exception as e:
        return handle_unexpected_error("retrieving budgets by category" , e)
    

def get_budgets_by_date_service(current_user , start_date , end_date):
    pass