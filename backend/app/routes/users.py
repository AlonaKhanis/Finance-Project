from datetime import datetime
from flask import Blueprint, jsonify, request
import pytz
from app.models import User, db
from werkzeug.security import generate_password_hash

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
def get_users():
    users = User.query.all()
    users_list = []
    for user in users:
        local_created_date = convert_to_local_time(user.created_date)
        users_list.append({
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'created_date': local_created_date.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(users_list), 200

@user_bp.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello from the user route'}), 200

@user_bp.route('/users', methods=['POST'])
def add_user():
    print('Request data:', request.data)
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password') 
    print(data)

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Create a new user instance
    new_user = User(username=username, email=email, password_hash=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201
