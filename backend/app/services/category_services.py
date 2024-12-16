from app.models import Category
from sqlalchemy.exc import SQLAlchemyError
from app.models import db

import logging
logger = logging.getLogger(__name__)


def get_all_categories():
    try:
        categories = Category.query.all()
        categories_list = []
        
        
        for category in categories:
            categories_list.append({
                'category_id': category.category_id,
                'name': category.name,
                'description': category.description,
                'created_date': category.created_date.strftime('%Y-%m-%d %H:%M:%S'),
            })
        return categories_list , 200
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        return {'error': 'Database error occurred. Please try again later.'}, 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {'error': 'An unexpected error occurred. Please try again later.'}, 500


def get_category_by_id_service(category_id):
    try:

        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            return {'error': 'Category not found.'}, 404

    
        return {
            'category_id': category.category_id,
            'name': category.name,
            'description': category.description,
            'created_date': category.created_date.strftime('%Y-%m-%d %H:%M:%S'),
        }, 200
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving category: {e}")
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except Exception as e:
        logger.error(f"Unexpected error retrieving category: {e}")
        return {'error': 'An unexpected error occurred. Please try again later.'}, 500

    
def add_category(data):
    try:
        name = data.get('name')
        description = data.get('description', '')

        if not name:
            return {'error': 'Category name is required.'}, 400

        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()

        return {
            'message': 'Category added successfully.',
            'category_id': category.category_id
        }, 201
    except SQLAlchemyError as e:
        logger.error(f"Database error adding category: {e}")
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except Exception as e:
        logger.error(f"Unexpected error adding category: {e}")
        return {'error': 'An unexpected error occurred. Please try again later.'}, 500
    

def update_category_service(category_id, data):
    try:
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            return {'error': 'Category not found.'}, 404
        category.name = data.get('name',category.name)
        category.description = data.get('description', category.description)
        db.session.commit()
        return {'message': 'Category updated successfully.'}, 200
    except SQLAlchemyError as e:
        logger.error(f"Database error updating category: {e}")
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except Exception as e:
        logger.error(f"Unexpected error updating category: {e}")
        return {'error': 'An unexpected error occurred. Please try again later.'}, 500
    

def delete_category_service(category_id):
    try:
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            return {'error': 'Category not found.'}, 404
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Category deleted successfully.'}, 200
    except SQLAlchemyError as e:
        logger.error(f"Database error deleting category: {e}")
        return {'error': 'Database error occurred. Please try again later.'}, 500
    except Exception as e:
        logger.error(f"Unexpected error deleting category: {e}")
        return {'error': 'An unexpected error occurred. Please try again later.'}, 500
    
    