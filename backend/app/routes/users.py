from flask import Blueprint, jsonify, request
from app.models import User, db
from werkzeug.security import generate_password_hash

user_bp = Blueprint('users', __name__)


@user_bp.route('/get_users', methods=['GET'])
def get_users():
    users = User.query.all()  # Now this works
    users_list = [
        {
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'created_date': user.created_date,
            
        }
        for user in users
    ]
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
