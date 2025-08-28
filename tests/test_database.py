import pytest
import sqlite3
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import database as db

@pytest.fixture
def test_db():
    """Fixture to set up and tear down a test database."""
    db.DB_FILE = "test_app.db"
    db.setup_database()
    yield
    os.remove(db.DB_FILE)

def test_create_user(test_db):
    """Test user creation and password hashing."""
    assert db.create_user("testuser", "password123")
    assert not db.create_user("testuser", "password123") # Test duplicate username

    user = db.get_user_by_username("testuser")
    assert user is not None
    assert user.username == "testuser"
    assert db.check_password("testuser", "password123")
    assert not db.check_password("testuser", "wrongpassword")

def test_insert_and_search_posts(test_db):
    """Test inserting and searching for posts."""
    db.create_user("testuser", "password123")
    user = db.get_user_by_username("testuser")

    posts_data = [
        {'url': 'http://insta.com/p/1', 'caption': 'caption one', 'likes': 10, 'comments': 1},
        {'url': 'http://insta.com/p/2', 'caption': 'caption two', 'likes': 20, 'comments': 2},
    ]

    db.insert_posts(user.id, "testuser", posts_data)

    # Test searching all posts
    all_posts = db.search_posts(user.id)
    assert len(all_posts) == 2

    # Test searching with a query
    caption_one_posts = db.search_posts(user.id, query="one")
    assert len(caption_one_posts) == 1
    assert caption_one_posts[0][2] == "caption one"

    # Test searching with a date
    # This is a bit tricky without mocking datetime, but we can check for results
    from datetime import date
    today = date.today().strftime("%Y-%m-%d")
    date_posts = db.search_posts(user.id, date_after=today)
    assert len(date_posts) == 2
