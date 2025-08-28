from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import src.plugin_manager as plugin_manager
import src.database as db

app = Flask(__name__)
app.secret_key = 'super-secret-key' # In a real app, this would be a secure, random key
socketio = SocketIO(app)
db.setup_database()
plugins = plugin_manager.load_plugins()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.get_user_by_id(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.check_password(username, password):
            user = db.get_user_by_username(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.create_user(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    posts = db.search_posts(current_user.id)
    return render_template('index.html', posts=posts, plugins=plugins.keys(), current_user=current_user)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', current_user=current_user)

from flask import jsonify
import sqlite3

@app.route('/api/v1/dashboard_data')
@login_required
def dashboard_data():
    # This is a simple example. A real implementation would be more complex.
    conn = sqlite3.connect(db.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, COUNT(*) FROM posts WHERE user_id = ? GROUP BY username", (current_user.id,))
    data = cursor.fetchall()
    conn.close()

    chart_data = {
        'labels': [row[0] for row in data],
        'datasets': [{
            'label': 'Posts per User',
            'data': [row[1] for row in data],
        }]
    }
    return jsonify(chart_data)


@socketio.on('fetch_posts')
def handle_fetch_posts_event(json):
    usernames = json.get('usernames')
    plugin_name = json.get('plugin')

    if usernames and plugin_name:
        plugin = plugins.get(plugin_name)
        if plugin:
            username_list = [u.strip() for u in usernames.split(',')]
            count = 0
            for username in username_list:
                count += 1
                socketio.emit('progress', {'msg': f'Fetching posts for {username}...', 'percent': (count / len(username_list)) * 100})
                posts = plugin.get_posts(username)
                if posts:
                    db.insert_posts(current_user.id, username, posts)
            socketio.emit('progress', {'msg': 'Finished fetching all posts.', 'percent': 100})

if __name__ == '__main__':
    socketio.run(app, debug=True)
