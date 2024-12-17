
from flask import  Blueprint, jsonify, request
from app.models import db
from app.services.auth_services import change_password_service, login_user, register_user, reset_password_service, verify_email_service
from werkzeug.exceptions import BadRequest

import logging
logger = logging.getLogger(__name__)
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = register_user(data)

    return jsonify(response), status_code



@auth_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Call the service layer
        result, status_code = verify_email_service(token)
        
        # Log the successful email verification access (User clicked on the link)
        if status_code == 200:
            logger.info(f"User accessed the email verification link for token: {token}")
        
        return jsonify(result), status_code
    
    except Exception as e:
        # Catch any unexpected errors
        logger.exception(f"Unexpected error during email verification: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response), status_code


@auth_bp.route('/change_password', methods=['PUT'])
def change_password(current_user):
        data = request.get_json()
        response, status_code = change_password_service(data, current_user, db)
        return jsonify(response), status_code



@auth_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        new_password = request.get_json().get('new_password')

        if not new_password:
            return jsonify({"error": "New password is required."}), 400

        response, status_code = reset_password_service(new_password, token)
        return jsonify(response), status_code

    except Exception as e:
        logger.exception(f"Unexpected error in reset_password route: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500



