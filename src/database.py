import sqlite3
from datetime import datetime

DB_FILE = "media_data.db"

def setup_database():
    """Initializes the database and creates the 'posts' table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            post_url TEXT NOT NULL UNIQUE,
            timestamp DATETIME NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_post(username, post_url):
    """Inserts a new post into the database."""
    conn = sqlite3.connect(DB_File)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO posts (username, post_url, timestamp)
            VALUES (?, ?, ?)
        """, (username, post_url, datetime.now()))
        conn.commit()
    except sqlite3.IntegrityError:
        # This error occurs if the post_url is not unique, which is fine.
        pass
    finally:
        conn.close()

def insert_posts(username, post_urls):
    """Inserts a list of posts for a given username."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    for url in post_urls:
        try:
            cursor.execute("""
                INSERT INTO posts (username, post_url, timestamp)
                VALUES (?, ?, ?)
            """, (username, url, datetime.now()))
        except sqlite3.IntegrityError:
            pass # Ignore duplicates
    conn.commit()
    conn.close()

def get_all_posts():
    """Retrieves all posts from the database."""
    return search_posts()

def search_posts(query=None, date_after=None, date_before=None):
    """
    Searches posts in the database based on a query and/or date range.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    sql_query = "SELECT username, post_url, timestamp FROM posts"
    conditions = []
    params = []

    if query:
        conditions.append("(username LIKE ? OR post_url LIKE ?)")
        params.extend([f"%{query}%", f"%{query}%"])

    if date_after:
        conditions.append("timestamp >= ?")
        params.append(date_after)

    if date_before:
        conditions.append("timestamp <= ?")
        params.append(date_before)

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

    sql_query += " ORDER BY timestamp DESC"

    cursor.execute(sql_query, params)
    posts = cursor.fetchall()
    conn.close()
    return posts
