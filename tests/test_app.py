import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from src import database as db

@pytest.fixture
def client():
    """Create and configure a new app instance for each test."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'testing'
    db.DB_FILE = "test_flask.db"
    db.setup_database()

    with app.test_client() as client:
        yield client

    import os
    os.remove(db.DB_FILE)

def test_auth_pages(client):
    """Test that login and register pages load."""
    assert client.get('/login').status_code == 200
    assert client.get('/register').status_code == 200

def test_index_redirect(client):
    """Test that the index page redirects if not logged in."""
    assert client.get('/').status_code == 302 # 302 is redirect

def test_register_and_login(client):
    """Test user registration and login."""
    # Register a new user
    rv = client.post('/register', data=dict(
        username='testuser',
        password='password123'
    ), follow_redirects=True)
    assert b'Registration successful' in rv.data

    # Log in with the new user
    rv = client.post('/login', data=dict(
        username='testuser',
        password='password123'
    ), follow_redirects=True)
    assert b'Welcome, testuser!' in rv.data
    assert client.get('/').status_code == 200 # Should now be accessible

def test_logout(client):
    """Test logging out."""
    # First, register and log in
    client.post('/register', data=dict(username='testuser', password='password123'))
    client.post('/login', data=dict(username='testuser', password='password123'))

    # Then, log out
    rv = client.get('/logout', follow_redirects=True)
    assert b'Login' in rv.data # Should be back on the login page
    assert client.get('/').status_code == 302 # Index should be protected again
