import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app.config import get_config
from app.routes import register_routes 
from app.models import db , migrate

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints or routes
    register_routes(app)  

    with app.app_context():
        if not app.config['TESTING']:
            db.create_all() 

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
