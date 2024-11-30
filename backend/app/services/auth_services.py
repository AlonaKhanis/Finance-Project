
from datetime import datetime, timedelta, timezone
from flask import current_app, url_for
from werkzeug.security import generate_password_hash
from app.models import User
import jwt
from email.mime.text import MIMEText
import smtplib
from werkzeug.exceptions import BadRequest



unverified_users = {}

def send_verification_email(email, verification_url):
    msg = MIMEText(f"Please verify your email by clicking on the following link: {verification_url}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'no-reply@example.com'  
    msg['To'] = email

    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)


def register_user(data , db):
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    role = data.get('role', 'user')

  
    if not email or not password or not first_name or not last_name:
        raise ValueError("All fields are required.")

   
    if User.query.filter_by(email=email).first():
        raise ValueError("Email already registered.")

 
    if email in unverified_users:
        raise ValueError("Email verification in progress. Please check your email.")

    # Generate verification token
    token = jwt.encode(
        {"email": email, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    
    unverified_users[email] = {
        "first_name": first_name,
        "last_name": last_name,
        "password_hash": generate_password_hash(password),
        "verification_token": token,
        "role": role,
    }

    # Create verification URL
    verification_url = url_for('auth.verify_email', token=token, _external=True)

    
    send_verification_email(email, verification_url)

    return {"message": "Email verification in progress."}, 201

def verify_email_service(token , db):
    try:
        # Decode the token
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        email = data['email']

        # Check if the email is in the temporary storage
        if email not in unverified_users:
            raise BadRequest("Invalid or expired verification token.")

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

        return {"message": "Email verified successfully! You can now log in."}

    except jwt.ExpiredSignatureError:
        raise BadRequest("Verification link has expired.")
    except jwt.InvalidTokenError:
        raise BadRequest("Invalid verification token.")
    

def login_user(data , db):    
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        raise ValueError("Invalid email or password.")

    token = jwt.encode(
        {"user_id": user.user_id, "role": user.role, "exp": datetime.now(timezone.utc) + timedelta(hours=10)},
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    return {"token": token}, 200 