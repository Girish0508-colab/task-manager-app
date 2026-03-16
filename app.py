from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"


# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# CREATE TABLES
# -------------------------
def init_db():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        deadline TEXT,
        priority TEXT,
        status TEXT,
        user_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


init_db()


# -------------------------
# DASHBOARD
# -------------------------
@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks WHERE user_id=?",
        (session["user_id"],)
    ).fetchall()

    pending = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Pending' AND user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    completed = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE status='Done' AND user_id=?",
        (session["user_id"],)
    ).fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        pending=pending,
        completed=completed
    )


# -------------------------
# REGISTER
# -------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = get_db()

        try:
            conn.execute(
                "INSERT INTO users(username,password) VALUES(?,?)",
                (username, password)
            )
            conn.commit()
        except:
            return "Username already exists"

        conn.close()

        return redirect("/login")

    return render_template("register.html")


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]

            return redirect("/")

        else:
            return "Invalid login"

    return render_template("login.html")


# -------------------------
# LOGOUT
# -------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# -------------------------
# ADD TASK (AI PRIORITY)
# -------------------------
@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]
    deadline = request.form["deadline"]

    # AI priority prediction
    text = title.lower()

    if "exam" in text or "deadline" in text or "urgent" in text:
        priority = "High"

    elif "study" in text or "project" in text:
        priority = "Medium"

    else:
        priority = "Low"

    conn = get_db()

    conn.execute(
        "INSERT INTO tasks(title,deadline,priority,status,user_id) VALUES(?,?,?,?,?)",
        (title, deadline, priority, "Pending", session["user_id"])
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# COMPLETE TASK
# -------------------------
@app.route("/complete/<int:id>")
def complete(id):

    conn = get_db()

    conn.execute(
        "UPDATE tasks SET status='Done' WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# DELETE TASK
# -------------------------
@app.route("/delete/<int:id>")
def delete(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# AI ASSISTANT
# -------------------------
@app.route("/assistant", methods=["POST"])
def assistant():

    message = request.json["message"].lower()

    if "priority" in message:
        reply = "High priority tasks should be completed first."

    elif "productivity" in message:
        reply = "Try the Pomodoro technique: 25 minutes work, 5 minutes break."

    elif "plan" in message:
        reply = "Start with the most important tasks and schedule breaks."

    else:
        reply = "Ask me about productivity, planning, or task priorities."

    return jsonify({"reply": reply})


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)