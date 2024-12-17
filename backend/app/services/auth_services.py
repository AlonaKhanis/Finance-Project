
from datetime import datetime, timedelta, timezone
from flask import current_app, url_for
from werkzeug.security import generate_password_hash
from app.models import User
import jwt
from email.mime.text import MIMEText
import smtplib
from werkzeug.exceptions import BadRequest
from app.models import db
from sqlalchemy.exc import SQLAlchemyError

import logging
logger = logging.getLogger(__name__)

# python -m smtpd -c DebuggingServer -n localhost:1025      



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


def register_user(data):
    try:
        # Extract user data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role', 'user')

        # Validate the required fields
        if not email or not password or not first_name or not last_name:
            raise ValueError("All fields are required.")

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            raise ValueError("Email already registered.")

        # Check if the email is currently in unverified users list
        if email in unverified_users:
            raise ValueError("Email verification in progress. Please check your email.")

        # Generate a verification token
        token = jwt.encode(
            {"email": email, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )

        validate_password_strength(password)

        # Store the user's data temporarily in the unverified_users dictionary
        unverified_users[email] = {
            "first_name": first_name,
            "last_name": last_name,
            "password_hash": generate_password_hash(password),
            "verification_token": token,
            "role": role,
        }

        # Generate the verification URL
        verification_url = url_for('auth.verify_email', token=token, _external=True)

        # Send the verification email
        send_verification_email(email, verification_url)

        return {"message": "Email verification in progress."}, 201

    except ValueError as ve:
        current_app.logger.warning(f"Registration error: {ve}")
        return {"error": str(ve)}, 400

    except jwt.ExpiredSignatureError:
        current_app.logger.error("JWT token has expired.")
        return {"error": "Expired token."}, 400

    except jwt.InvalidTokenError:
        current_app.logger.error("Invalid JWT token.")
        return {"error": "Invalid token."}, 400

    except Exception as e:
        # Catch any unexpected errors
        current_app.logger.exception(f"Unexpected error during registration: {e}")
        return {"error": "An unexpected error occurred. Please try again later."}, 500


def verify_email_service(token):
    try:
        # Decode the JWT token
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        email = data['email']

        # Check if email is in unverified_users
        if email not in unverified_users:
            return {"error": "Invalid or expired verification token."}, 400

        # Get the user info from the unverified users
        user_info = unverified_users[email]
        user = User(
            first_name=user_info['first_name'],
            last_name=user_info['last_name'],
            email=email,
            password_hash=user_info['password_hash'],
            role=user_info['role'],
        )

        # Add user to the database
        db.session.add(user)
        db.session.commit()

        # Remove the user from the unverified_users list
        del unverified_users[email]

        # Return success message
        return {"message": "Email verified successfully! You can now log in."}, 200

    except jwt.ExpiredSignatureError:
        logger.warning("Verification link has expired.")
        return {"error": "Verification link has expired."}, 400
    except jwt.InvalidTokenError:
        logger.warning("Invalid verification token.")
        return {"error": "Invalid verification token."}, 400
    except Exception as e:
        logger.exception(f"Unexpected error during email verification: {e}")
        return {"error": "An unexpected error occurred during email verification."}, 500

    

def login_user(data):
    try:
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            logger.warning("Login attempt with missing email or password.")
            raise ValueError("Email and password are required.")

        user = User.query.filter_by(email=email).first()

        if user is None:
            logger.warning(f"Login failed: User with email {email} not found.")
            raise ValueError("Invalid email or password.")

        if not user.check_password(password):
            logger.warning(f"Login failed: Invalid password for user {email}.")
            raise ValueError("Invalid email or password.")

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": user.user_id,
                "role": user.role,
                "exp": datetime.now(timezone.utc) + timedelta(hours=10)
            },
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )

        logger.info(f"User {email} logged in successfully.")
        return {"token": token}, 200

    except ValueError as e:
        logger.error(f"Login error: {str(e)}")
        return {"error": str(e)}, 400 
    except Exception as e:
        logger.exception("Unexpected error during login.") 
        return {"error": "An unexpected error occurred. Please try again later."}, 500


def change_password_service(data , current_user):
    try:    
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not current_user.check_password(old_password):
            raise ValueError("Invalid password.")

        validate_password_strength(new_password)

        if current_user.check_password(new_password):
            raise ValueError("New password is invalid. Please try a different password.")
            

        current_user.set_password(new_password)
        db.session.commit()

        return {"message": "Password changed successfully."}, 200
    except ValueError as ve:
        logger.warning(f"Password change failed: {str(ve)}")
        return {"error": str(ve)}, 400
    except SQLAlchemyError as sae:
        logger.error(f"Database error while changing password: {sae}")
        return {"error": "A database error occurred. Please try again later."}, 500   
    except Exception as e:
        logger.exception("Unexpected error during password change.")
        return {"error": "An unexpected error occurred. Please try again later."}, 500    


def reset_password_service(new_password, token):
    """
    Service function to validate a reset token and update the user's password.
    """
    try:
        
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        logger.info(f"Decoded token data: {data}")  
        user_id = data.get('user_id')

        if not user_id:
            raise ValueError("Invalid or expired reset token.")

        
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            raise ValueError("User not found with the provided reset token.")

        logger.info(f"User found: {user_id}") 
        
        validate_password_strength(new_password)

       
        user.set_password(new_password) 
        db.session.commit()

        logger.info(f"Password reset attempt for user {user_id}")
        return {"message": "Password reset successfully."}, 200

   
    except jwt.ExpiredSignatureError:
        logger.warning("Reset token has expired.")
        return {"error": "The reset link has expired."}, 400
    except jwt.InvalidTokenError:
        logger.warning("Invalid reset token.")
        return {"error": "Invalid reset token."}, 400
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        return {"error": str(ve)}, 400
    except SQLAlchemyError as se:
        logger.error(f"Database error: {se}")
        db.session.rollback()
        return {"error": "A database error occurred. Please try again later."}, 500
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return {"error": "An unexpected error occurred. Please try again later."}, 500


def validate_password_strength(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
