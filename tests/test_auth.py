import pytest
from unittest.mock import patch, MagicMock

def test_register_user(client):
    # Mock UserModel.get_by_email to return None (user doesn't exist)
    with patch('app.models.user.UserModel.get_by_email', return_value=None), \
         patch('app.models.user.UserModel.get_by_unique_id', return_value=None), \
         patch('app.models.user.UserModel.create') as mock_create:
        
        mock_create.return_value = {
            'id': '123',
            'name': 'Test User',
            'email': 'test@example.com',
            'course': 'CS101',
            'unique_id': 'U101'
        }
        
        response = client.post('/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'course': 'CS101',
            'unique_id': 'U101'
        })
        
        assert response.status_code == 201
        assert response.json['user']['email'] == 'test@example.com'

def test_login_user(client):
    with patch('app.models.user.UserModel.get_by_email') as mock_get:
        # Mock user with hashed password
        from app.extensions import bcrypt
        pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        
        mock_get.return_value = {
            'id': '123',
            'name': 'Test User',
            'email': 'test@example.com',
            'password_hash': pw_hash,
            'course': 'CS101',
            'unique_id': 'U101'
        }
        
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 200
        assert 'access_token' in response.json

def test_login_invalid_password(client):
    with patch('app.models.user.UserModel.get_by_email') as mock_get:
        from app.extensions import bcrypt
        pw_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
        
        mock_get.return_value = {
            'id': '123',
            'email': 'test@example.com',
            'password_hash': pw_hash
        }
        
        response = client.post('/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
