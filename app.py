from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# -------------------------
# DATABASE CONNECTION
# -------------------------

def get_db_connection():
    conn = sqlite3.connect("job_tracker.db")
    conn.row_factory = sqlite3.Row
    return conn


# -------------------------
# CREATE DATABASE TABLE
# -------------------------

conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.commit()
conn.close()


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def index():

    conn = get_db_connection()

    applications = conn.execute(
        "SELECT * FROM applications"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        applications=applications
    )


# -------------------------
# ADD APPLICATION
# -------------------------

@app.route("/add", methods=["POST"])
def add_application():

    company = request.form["company"]
    role = request.form["role"]
    location = request.form["location"]
    status = request.form["status"]

    conn = get_db_connection()

    conn.execute("""
        INSERT INTO applications
        (company, role, location, status)
        VALUES (?, ?, ?, ?)
    """, (company, role, location, status))

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# EDIT APPLICATION
# -------------------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):

    conn = get_db_connection()

    # Save edited information
    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        location = request.form["location"]
        status = request.form["status"]

        conn.execute("""
            UPDATE applications
            SET company = ?, role = ?, location = ?, status = ?
            WHERE id = ?
        """, (company, role, location, status, id))

        conn.commit()
        conn.close()

        return redirect("/")

    # Get existing application
    application = conn.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        "edit.html",
        application=application
    )


# -------------------------
# DELETE APPLICATION
# -------------------------

@app.route("/delete/<int:id>")
def delete_application(id):

    conn = get_db_connection()

    conn.execute(
        "DELETE FROM applications WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# -------------------------
# RUN FLASK
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)