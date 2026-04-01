import sqlite3
from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'password123')")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/secure")
def secure():
    return render_template("login_secure.html")

@app.route("/login", methods=["POST"])
def login_vulnerable():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(query)
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful! (vulnerable route)"
    else:
        return "Invalid credentials. (vulnerable route)"

@app.route("/login-secure", methods=["POST"])
def login_secure():
    username = request.form["username"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful! (secure route)"
    else:
        return "Invalid credentials. (secure route)"
    
@app.route("/search")
def search():
    query = request.args.get("query", "")
    if query:
        return f"<p>Search results for: {query}</p>"
    return render_template("search.html")

@app.route("/search-secure")
def search_secure():
    query = request.args.get("query", "")
    return render_template("search_secure.html", query=query)

init_db()
app.run(debug=True)