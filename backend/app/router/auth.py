
from flask import  Blueprint, jsonify, request
from app.models import db
from app.services.auth_services import change_password_service, login_user, register_user, reset_password_service, verify_email_service
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


@auth_bp.route('/change_password', methods=['PUT'])
def change_password(current_user):
    
    try:
        data = request.get_json()
        change_password_service(data, current_user, db)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400    

    return jsonify({"message": "Password changed successfully."}), 200


@auth_bp.route('/resrt_password/<token>', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = request.args.get('token')
    new_password = data.get('new_password')
    
    if not token or not new_password:
            return jsonify({"error": "Token and new password are required."}), 400

    return reset_password_service(new_password, token, db)
