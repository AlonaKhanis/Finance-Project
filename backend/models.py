from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Users Table
class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)
    profile_picture = Column(String)

    expenses = relationship('Expense', back_populates='user')
    budgets = relationship('Budget', back_populates='user')
    goals = relationship('Goal', back_populates='user')
    notifications = relationship('Notification', back_populates='user')
    logs = relationship('AuditLog', back_populates='user')

# Categories Table
class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'income' or 'expense'
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship('User')
    expenses = relationship('Expense', back_populates='category')

# Expenses Table
class Expense(Base):
    __tablename__ = 'expenses'
    expense_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)
    is_recurring = Column(Boolean, default=False)

    user = relationship('User', back_populates='expenses')
    category = relationship('Category', back_populates='expenses')

# Budgets Table
class Budget(Base):
    __tablename__ = 'budgets'
    budget_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)
    amount = Column(Float, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='budgets')
    category = relationship('Category')

# Goals Table
class Goal(Base):
    __tablename__ = 'goals'
    goal_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, nullable=False)
    deadline = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='goals')

# Notifications Table
class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message = Column(String, nullable=False)
    type = Column(String)  # 'budget alert', 'income alert', etc.
    is_read = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='notifications')

# Audit Logs Table
class AuditLog(Base):
    __tablename__ = 'audit_logs'
    log_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    action = Column(String, nullable=False)  # 'created transaction', 'updated budget', etc.
    next_occurrence = Column(DateTime)
    table_name = Column(String)
    record_id = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='logs')

# Recurring Transactions Table
class RecurringTransaction(Base):
    __tablename__ = 'recurring_transactions'
    recurring_transaction_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('expenses.expense_id'), nullable=False)
    interval = Column(String, nullable=False)  # 'daily', 'weekly', 'monthly'
    next_occurrence = Column(DateTime)
    end_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, onupdate=datetime.utcnow)

# Attachments Table
class Attachment(Base):
    __tablename__ = 'attachments'
    attachment_id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('expenses.expense_id'), nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

# Create an engine
engine = create_engine('sqlite:///finances.db')

# Create all tables
Base.metadata.create_all(engine)
