from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app, url_for, Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from app.models import User , db
import smtplib
from email.mime.text import MIMEText

auth_bp = Blueprint('auth', __name__)

unverified_users = {}

def send_verification_email(email, verification_url):
    msg = MIMEText(f"Please verify your email by clicking on the following link: {verification_url}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'no-reply@example.com'  
    msg['To'] = email

    # Use the local debugging SMTP server
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role', 'user')
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered."}), 400

    # Check if the email is already pending verification
    if email in unverified_users:
        return jsonify({"error": "Email verification in progress. Please check your email."}), 400

    # Generate verification token
    token = jwt.encode(
        {"email": email, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},  #
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    # Store user details temporarily
    unverified_users[email] = {
        "first_name": first_name,
        "last_name": last_name,
        "password_hash": generate_password_hash(password),
        "verification_token": token,
        "role": role,
    }

    # Generate verification URL
    verification_url = url_for('auth.verify_email', token=token, _external=True)
    send_verification_email(email, verification_url)

    return jsonify({"message": "Email verification in progress."}), 201


@auth_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        email = data['email']

        # Check if the email is in the temporary storage
        if email not in unverified_users:
            return jsonify({"error": "Invalid or expired verification token."}), 400

        # Create the user in the database
        user_info = unverified_users[email]
        user = User(
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            email=email,
            password_hash=user_info['password_hash'],
            role=user_info['role'],
        )

        db.session.add(user)
        db.session.commit()

        # Remove from temporary storage
        del unverified_users[email]

        return jsonify({"message": "Email verified successfully! You can now log in."}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Verification link has expired."}), 400
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid verification token."}), 400
    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    
    token = jwt.encode(
        {"user_id": user.user_id, "role": user.role, "exp": datetime.now(timezone.utc) + timedelta(hours=10)},
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return jsonify({"token": token}), 200

