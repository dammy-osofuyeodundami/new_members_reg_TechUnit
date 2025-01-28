from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "members.db"

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            level TEXT NOT NULL,
            matric_no TEXT NOT NULL,
            registration_no TEXT NOT NULL,
            course TEXT NOT NULL,
            biography TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    conn.close()
    return render_template("index.html", members=members)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        gender = request.form["gender"]
        level = request.form["level"]
        matric_no = request.form["matric_no"]
        registration_no = request.form["registration_no"]
        course = request.form["course"]
        biography = request.form["biography"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO members (name, gender, level, matric_no, registration_no, course, biography)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, gender, level, matric_no, registration_no, course, biography))
        conn.commit()
        conn.close()

        return redirect(url_for("success"))
    return render_template("register.html")

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    init_db()  # Initialize the database on startup
    app.run(debug=False)
