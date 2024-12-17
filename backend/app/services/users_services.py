
from datetime import datetime
import pytz
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.models import db
import logging

logger = logging.getLogger(__name__)


def convert_to_local_time(utc_dt, tz_name=None):
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    if tz_name:
        local_tz = pytz.timezone(tz_name)
    else:
        local_tz = datetime.now().astimezone().tzinfo
    return utc_dt.astimezone(local_tz)

def get_all_users():
    try:
        users = User.query.all()
        users_list = []
        
        for user in users:
            local_created_date = convert_to_local_time(user.created_date)
            users_list.append(
                {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'role': user.role,
                }
            )
        logger.info(f"User list has been fetched successfully. Total users: {len(users_list)}")
        return users_list , 200
    
    except SQLAlchemyError as se:
        logger.error(f"Database error: {se}")
        return {"error": "Database error occurred."}, 500
    
    except Exception as e:
        logger.exception(f"Unexpected error fetching users: {e}")
        return {"error": "An unexpected error occurred."}, 500
 

def get_user_by_id_service(user_id):
    
    try:
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            logger.warning(f"No user found with user_id: {user_id}")
            return {"error": "User not found."}, 404
        
        local_created_date = convert_to_local_time(user.created_date)
        user_info = {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'role': user.role,
        }

        logger.info(f"User {user_id} fetched successfully")
        return user_info , 200
    
    except SQLAlchemyError as se:
        logger.erro(f"Database error while fetching user {user_id}:{se}")
        return {"error" : "Database error occurres"} , 500
    except Exception as e:
        logger.exception(f"Unexpected error fetching user {user_id} : {e}")
        return {"error" : "An unexpected error occurred"} , 500

    
def update_user_service(user_id, data):
    try:
       
        user = User.query.filter_by(user_id=user_id).first()

        if user is None:
            logger.warning(f"No user found with user_id: {user_id}")
            return {"error": "User not found."}, 404

  
        new_email = data.get('email')
        if new_email and new_email != user.email:
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user:
                logger.warning(f"Email '{new_email}' already exists for another user.")
                return {"error": "Email already exists."}, 409  

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = new_email or user.email
        user.role = data.get('role', user.role)

        db.session.commit()
        logger.info(f"User {user_id} updated successfully.")
        return {"message": "User updated successfully."}, 200

    except SQLAlchemyError as se:
        db.session.rollback()
        logger.error(f"Database error while updating user {user_id}: {se}")
        return {"error": "Database error occurred."}, 500

    except Exception as e:
        db.session.rollback()
        logger.exception(f"Unexpected error updating user {user_id}: {e}")
        return {"error": "An unexpected error occurred."}, 500
    

def delete_user_service(user_id):
    try:
        user = User.query.filter_by(user_id=user_id).first()
        
        if user is None:
            logger.warning(f"No user found with user_id: {user_id}")
            return {"error": "User not found."}, 404
        
        
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User {user_id} deleted successfully.")
        return {"message": "User deleted successfully."}, 200
    
    except SQLAlchemyError as se:
        db.session.rollback()
        logger.error(f"Database error while deleting user {user_id}: {se}")
        return {"error": "Database error occurred."}, 500
    
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Unexpected error deleting user {user_id}: {e}")
        return {"error": "An unexpected error occurred."}, 500




    