from datetime import datetime, timedelta, timezone
import jwt
from flask import current_app, Blueprint, jsonify, request
from app.models import User , db
from email.mime.text import MIMEText
from app.services.auth_services import login_user, register_user, verify_email_service
from werkzeug.exceptions import BadRequest

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        response, status_code = register_user(data , db)
        return jsonify(response), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@auth_bp.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Call the service layer
        result = verify_email_service(token, db)
        return jsonify(result), 200
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        response, status_code = login_user(data , db)
        return jsonify(response), status_code
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
