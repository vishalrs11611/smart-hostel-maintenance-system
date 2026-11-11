"""Smart Hostel Maintenance System - Flask application with SQLite storage."""
import os
import sqlite3
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for

COMPLAINT_CATEGORIES = (
    "Water Supply",
    "Electricity",
    "Plumbing",
    "Cleaning",
    "Other",
)
COMPLAINT_STATUSES = ("Pending", "In Progress", "Resolved")

SCHEMA = """
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT NOT NULL,
    category TEXT NOT NULL CHECK (
        category IN ('Water Supply', 'Electricity', 'Plumbing', 'Cleaning', 'Other')
    ),
    description TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending' CHECK (
        status IN ('Pending', 'In Progress', 'Resolved')
    ),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

app = Flask(__name__)
app.config.from_mapping(
    DATABASE=os.environ.get(
        "SHMS_DATABASE",
        str(Path(app.instance_path) / "complaints.sqlite3"),
    )
)


def get_db():
    """Return the SQLite connection for the current application context."""
    if "db" not in g:
        database_path = app.config["DATABASE"]
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(database_path)
        connection.row_factory = sqlite3.Row
        g.db = connection
    return g.db


@app.teardown_appcontext
def close_db(_exception=None):
    """Close the request-scoped SQLite connection."""
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db():
    """Create the complaint table if it does not already exist."""
    get_db().executescript(SCHEMA)


@app.before_request
def ensure_database():
    """Ensure the schema exists before handling a request."""
    init_db()


@app.get("/")
def home():
    """Render the student form, warden table, and summary dashboard."""
    db = get_db()
    complaint_rows = db.execute(
        """
        SELECT id, student, category, description, status, created_at
        FROM complaints
        ORDER BY id DESC
        """
    ).fetchall()

    status_rows = db.execute(
        "SELECT status, COUNT(*) AS count FROM complaints GROUP BY status"
    ).fetchall()
    status_counts = {row["status"]: row["count"] for row in status_rows}
    total = db.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]

    return render_template(
        "index.html",
        complaints=complaint_rows,
        categories=COMPLAINT_CATEGORIES,
        statuses=COMPLAINT_STATUSES,
        total=total,
        pending=status_counts.get("Pending", 0),
        progress=status_counts.get("In Progress", 0),
        resolved=status_counts.get("Resolved", 0),
    )


@app.post("/submit")
def submit():
    """Validate and persist a new complaint."""
    student = request.form.get("student", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()

    if not student or not category or not description:
        abort(400, description="Please fill all fields.")

    if category not in COMPLAINT_CATEGORIES:
        abort(400, description="Please select a valid complaint category.")

    db = get_db()
    db.execute(
        """
        INSERT INTO complaints (student, category, description, status)
        VALUES (?, ?, ?, 'Pending')
        """,
        (student, category, description),
    )
    db.commit()
    return redirect(url_for("home"))


@app.post("/update/<int:complaint_id>")
def update(complaint_id):
    """Update a complaint status by its stable database ID."""
    new_status = request.form.get("status", "")
    if new_status not in COMPLAINT_STATUSES:
        abort(400, description="Please select a valid complaint status.")

    db = get_db()
    cursor = db.execute(
        "UPDATE complaints SET status = ? WHERE id = ?",
        (new_status, complaint_id),
    )
    if cursor.rowcount == 0:
        abort(404, description="Complaint not found.")

    db.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Colab uses the separate iframe launcher documented in README.md.
    app.run(host="127.0.0.1", port=5000, debug=False)
