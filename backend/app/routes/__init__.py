
from flask import Blueprint
from .users import user_bp  

main = Blueprint('main', __name__)


def register_routes(app):
    app.register_blueprint(user_bp)
