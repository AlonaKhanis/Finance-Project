import pytest
from flask import json
from app import create_app, db  

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client 
        with app.app_context():
            db.drop_all()

def test_create_user(client):
    """Test the user creation endpoint."""
    response = client.post('/users', 
                            data=json.dumps({
                                "username": "john_doe", 
                                "email": "john@example.com", 
                                "password": "securepassword123"
                            }), 
                            content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['message'] == "User added successfully"

def test_get_users(client):
    """Test retrieving users."""
    # Create a user first
    client.post('/users', 
                 data=json.dumps({
                     "username": "john_doe", 
                     "email": "john@example.com", 
                     "password": "securepassword123"
                 }), 
                 content_type='application/json')

    response = client.get('/users')
    
    assert response.status_code == 200 
    assert len(response.json) > 0 
