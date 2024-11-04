from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_migrate import Migrate
import pytz
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False) 
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True) 
    password_hash = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    profile_picture = db.Column(db.String)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String, nullable=True)
    role = db.Column(db.String, default='user')

    # Relationships
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)
    categories = db.relationship('Category', backref='user', lazy=True)
    goals = db.relationship('Goal', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    budgets = db.relationship('Budget', backref='user', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action = db.Column(db.String, nullable=False)
    next_occurrence = db.Column(db.DateTime)
    table_name = db.Column(db.String)
    record_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    budgets = db.relationship('Budget', backref='category', lazy=True)
    expenses = db.relationship('Expense', backref='category', lazy=True)

class Goal(db.Model):
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.String, nullable=False)
    type = db.Column(db.String)
    is_read = db.Column(db.Boolean)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Budget(db.Model):
    __tablename__ = 'budgets'

    budget_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))

class Expense(db.Model):
    __tablename__ = 'expenses'

    expense_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))
    is_recurring = db.Column(db.Boolean)

    # Relationships
    attachments = db.relationship('Attachment', backref='expense', lazy=True)
    recurring_transactions = db.relationship('RecurringTransaction', backref='expense', lazy=True)

class Attachment(db.Model):
    __tablename__ = 'attachments'

    attachment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('expenses.expense_id'), nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class RecurringTransaction(db.Model):
    __tablename__ = 'recurring_transactions'

    recurring_transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('expenses.expense_id'), nullable=False)
    interval = db.Column(db.String, nullable=False)
    next_occurrence = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    created_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, onupdate=lambda: datetime.now(timezone.utc))