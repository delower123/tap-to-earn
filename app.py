from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "users.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""CREATE TABLE users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            points INTEGER DEFAULT 0
        )""")
        conn.commit()
        conn.close()

def add_point(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users(username, points) VALUES(?,0)", (username,))
    c.execute("UPDATE users SET points = points + 1 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_points(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        add_point(username)
        points = get_points(username)
        return render_template('index.html', username=username, points=points)
    return render_template('index.html', username=None, points=None)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
