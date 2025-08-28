import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = "media_data.db"

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

def setup_database():
    """Initializes the database and creates tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            post_url TEXT NOT NULL,
            caption TEXT,
            likes INTEGER,
            comments_count INTEGER,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE(user_id, post_url)
        )
    """)
    # Add columns if they don't exist, for backwards compatibility
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN caption TEXT")
    except sqlite3.OperationalError: pass # column already exists
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN likes INTEGER")
    except sqlite3.OperationalError: pass
    try:
        cursor.execute("ALTER TABLE posts ADD COLUMN comments_count INTEGER")
    except sqlite3.OperationalError: pass
    conn.commit()
    conn.close()

def create_user(username, password):
    """Creates a new user with a hashed password."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, generate_password_hash(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False # Username already exists
    finally:
        conn.close()
    return True

def get_user_by_username(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1])
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[0], user_data[1])
    return None

def check_password(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    if record and check_password_hash(record[0], password):
        return True
    return False

def insert_posts(user_id, username, posts_data):
    """Inserts a list of posts for a given user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for post in posts_data:
        try:
            cursor.execute("""
                INSERT INTO posts (user_id, username, post_url, caption, likes, comments_count, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, username, post['url'], post['caption'], post['likes'], post['comments'], datetime.now()))
        except sqlite3.IntegrityError:
            pass # Ignore duplicates for the same user
    conn.commit()
    conn.close()

def search_posts(user_id, query=None, date_after=None, date_before=None):
    """
    Searches posts in the database for a specific user.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    sql_query = "SELECT username, post_url, caption, likes, comments_count, timestamp FROM posts WHERE user_id = ?"
    conditions = []
    params = [user_id]

    if query:
        conditions.append("(username LIKE ? OR post_url LIKE ? OR caption LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])

    if date_after:
        conditions.append("timestamp >= ?")
        params.append(date_after)

    if date_before:
        conditions.append("timestamp <= ?")
        params.append(date_before)

    if conditions:
        sql_query += " AND " + " AND ".join(conditions)

    sql_query += " ORDER BY timestamp DESC"

    cursor.execute(sql_query, params)
    posts = cursor.fetchall()
    conn.close()
    return posts
