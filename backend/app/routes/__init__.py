
from flask import Blueprint
from .users import user_bp  
from .auth import auth_bp
from .reset_password import reset_password_bp
from .expenses import expense_bp

main = Blueprint('main', __name__)


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reset_password_bp)
    app.register_blueprint(expense_bp)
    
