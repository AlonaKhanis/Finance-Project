from app import db
from app.models import Category

def seed_categories():
    categories = [
        { "name": "Groceries", "type": "Expense", "description": "Groceries for daily needs"},
        { "name": "Health", "type": "Expense", "description": "Medical and health-related expenses"},
    ]
    for category in categories:
        existing = Category.query.filter_by(name=category["name"], user_id=category["user_id"]).first()
        if not existing:
            db.session.add(Category(**category))
    db.session.commit()
