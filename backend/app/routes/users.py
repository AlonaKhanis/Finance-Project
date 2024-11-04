from datetime import datetime
from flask import Blueprint, jsonify, request
import pytz
from app.models import User
from .admin_route import role_required

user_bp = Blueprint('users', __name__)


def convert_to_local_time(utc_dt, tz_name=None):
    if utc_dt.tzinfo is None:
        utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    if tz_name:
        local_tz = pytz.timezone(tz_name)
    else:
        local_tz = datetime.now().astimezone().tzinfo
    return utc_dt.astimezone(local_tz)

@user_bp.route('/get_users', methods=['GET'])
@role_required('admin')
def get_users(current_user): 
    users = User.query.all()
    users_list = []
    for user in users:
        local_created_date = convert_to_local_time(user.created_date)
        users_list.append({
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(users_list), 200


