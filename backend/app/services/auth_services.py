
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


def send_password_reset_email(email, reset_token):
    smtp_server = "localhost"
    smtp_port = 1025
    sender_email = "no-reply@example.com"

    reset_url = f"http://localhost:5000/reset_password/{reset_token}"
    body = f"Click the link to reset your password: {reset_url}"

    msg = MIMEText(body, 'plain')
    msg['Subject'] = "Password Reset Request"
    msg['From'] = sender_email
    msg['To'] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.sendmail(sender_email, email, msg.as_string())
        print(f"Simulated email sent to {email}")


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

    
    verification_url = url_for('auth.verify_email', token=token, _external=True)

    
    send_verification_email(email, verification_url)

    return {"message": "Email verification in progress."}, 201

def verify_email_service(token , db):
    try:
        
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        email = data['email']

        
        if email not in unverified_users:
            raise BadRequest("Invalid or expired verification token.")

        
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



def change_password_service(data , current_user , db):
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not current_user.check_password(old_password):
        raise ValueError("Invalid password.")

    current_user.set_password(new_password)
    db.session.commit()

    return {"message": "Password changed successfully."}, 200

def reset_password_service(new_password , token , db):
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']

        if user_id is None:
            raise BadRequest("Invalid or expired reset token.")
        
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            raise BadRequest("Invalid user.")
        
        user.set_password(new_password)
        db.session.commit()

        
        print(f"Password reset for user {user_id}")
        return {"message": "Password reset successfully."}, 200
    
    except jwt.ExpiredSignatureError:
        raise BadRequest("Reset link has expired.")
    except jwt.InvalidTokenError:
        raise BadRequest("Invalid reset token.")
    except Exception as e:
        raise BadRequest(f"An unexpected error occurred: {str(e)}")