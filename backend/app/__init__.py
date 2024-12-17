import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from dotenv import load_dotenv

from .router import register_routes
from .config import get_config
from app.models import db, Category

import logging
from logging import StreamHandler
import sys


load_dotenv()

def create_initial_categories():
    existing_categories = Category.query.all()
    if not existing_categories:
        initial_categories = [
            Category(name='Technology', description='Tech-related expenses', is_global=True),
            Category(name='Health', description='Healthcare-related expenses', is_global=True),
            Category(name='Finance', description='Finance-related expenses', is_global=True),
            Category(name='Education', description='Education-related expenses', is_global=True),
            Category(name='Entertainment', description='Entertainment-related expenses', is_global=True)
        ]
        db.session.bulk_save_objects(initial_categories)
        db.session.commit()
        app.logger.info("Initial categories created successfully.")



def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.DEBUG, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    
    db.init_app(app)
    register_routes(app)

 
    with app.app_context():
        if not app.config['TESTING']:
            db.create_all()
            create_initial_categories()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
