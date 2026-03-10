from flask import Flask, render_template, request, redirect, session, jsonify, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE PATH
DB_PATH = os.path.join(os.getcwd(), "tasks.db")


# CONNECT DATABASE
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE TABLE
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT DEFAULT 'todo',
        due_date TEXT
    )
    """)

    conn.commit()
    conn.close()


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # simple demo login
        if username and password:
            session["user"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        return redirect(url_for("login"))

    return render_template("register.html")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    cursor = conn.cursor()

    tasks = cursor.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    todo = [t for t in tasks if t["status"] == "todo"]
    progress = [t for t in tasks if t["status"] == "progress"]
    done = [t for t in tasks if t["status"] == "done"]

    return render_template(
        "dashboard.html",
        todo=todo,
        progress=progress,
        done=done,
        tasks=tasks
    )


# ADD TASK
@app.route("/add_task", methods=["POST"])
def add_task():

    if "user" not in session:
        return redirect(url_for("login"))

    title = request.form["title"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, status, due_date) VALUES (?, ?, ?)",
        (title, status, due_date)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# UPDATE TASK STATUS
@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# DELETE TASK
@app.route("/delete_task/<int:id>")
def delete_task(id):

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)