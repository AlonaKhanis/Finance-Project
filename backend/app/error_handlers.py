from app.models import db
import logging
from flask import current_app

logger = logging.getLogger(__name__)

# error_handlers.py
def handle_db_error(operation, error):
    """Handles database errors and logs them consistently."""
    db.session.rollback()
    current_app.logger.error(f"Database error during {operation}: {error}")
    return {'error': 'Database error occurred. Please try again later.'}, 500

def handle_unexpected_error(operation, error):
    """Handles unexpected errors and logs them consistently."""
    db.session.rollback()
    current_app.logger.error(f"Unexpected error during {operation}: {error}")
    return {'error': 'An unexpected error occurred. Please try again later.'}, 500
