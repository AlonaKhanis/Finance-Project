
from flask import Blueprint
from .users import user_bp  
from .auth import auth_bp

main = Blueprint('main', __name__)


def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
