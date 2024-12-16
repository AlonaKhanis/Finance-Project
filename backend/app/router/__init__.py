
from flask import Blueprint
from app.router.users import user_bp
from app.router.auth import auth_bp
from app.router.reset_password import reset_password_bp
from app.router.expenses import expense_bp
from app.router.users import user_bp
from app.router.category import category_bp

main = Blueprint('main', __name__)


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(reset_password_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(category_bp)
    
