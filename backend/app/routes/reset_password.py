import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, jsonify, request, url_for, current_app
import jwt
from datetime import datetime, timedelta, timezone
from app.models import User, db

reset_password_bp = Blueprint('reset_password', __name__)

def send_reset_email(email, reset_url):
    
    msg = MIMEText(f"Click the link to reset your password: {reset_url}")
    msg['Subject'] = 'Password Reset Request'
    msg['From'] = 'no-reply@example.com'  
    msg['To'] = email

    
    with smtplib.SMTP('localhost', 1025) as server:
        server.send_message(msg)

@reset_password_bp.route('/request_reset', methods=['POST'])
def request_reset():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found."}), 404

    token = jwt.encode(
        {"user_id": user.user_id, "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        current_app.config['SECRET_KEY'],
        algorithm="HS256"
    )

    reset_url = url_for('reset_password.reset_password', token=token, _external=True)

    send_reset_email(email, reset_url)

    return jsonify({"message": "Password reset email sent."}), 200

@reset_password_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'GET':
        try:
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({"error": "Invalid token or user not found."}), 400
            
            return jsonify({"message": "Token is valid. Proceed to reset your password."}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "The token has expired."}), 400
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token."}), 400

    elif request.method == 'POST':
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.get(data['user_id'])

            if not user:
                return jsonify({"error": "Invalid token or user not found."}), 400

            new_password = request.get_json().get('new_password')
            if not new_password:
                return jsonify({"error": "New password is required."}), 400

            user.set_password(new_password)
            db.session.commit()

            return jsonify({"message": "Password has been reset successfully."}), 200

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "The token has expired."}), 400
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token."}), 400

