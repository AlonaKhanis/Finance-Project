
from datetime import datetime
import pytz

from app.models import User


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
        
        return users_list
    
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []
    

def fetch_user_by_id(user_id):
    print(user_id)
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        return None
    
    local_created_date = convert_to_local_time(user.created_date)
    try:
        user_info = {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'role': user.role,
        }

        return user_info
    
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None



def update_User(user_id, data , db):
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        return False

    try:
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
        db.session.commit()
        return True
    
    except Exception as e:
        print(f"Error updating user: {e}")
        return False
    

def delete_User(user_id, db):
    user = User.query.filter_by(user_id=user_id).first()
    
    if user is None:
        return False
    
    try:
        db.session.delete(user)
        db.session.commit()
        return True
    
    except Exception as e:
        print(f"Error deleting user: {e}")


def get_User_profile(current_user):

    local_created_date = convert_to_local_time(current_user.created_date)

    try:
        user_profile = {
            'user_id': current_user.user_id,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }

        return user_profile
        
    except Exception as e:
        print(f"Error fetching user profile: {e}")
        return None
    

    