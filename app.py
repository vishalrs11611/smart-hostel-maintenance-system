"""Smart Hostel Maintenance System - Flask application.

This is the baseline prototype: complaint data is held in memory and is
therefore lost when the process stops. Database persistence, authentication,
staff assignment, and runtime AI classification are tracked as future work.
"""
from flask import Flask, abort, redirect, render_template, request, url_for

COMPLAINT_CATEGORIES = (
    "Water Supply",
    "Electricity",
    "Plumbing",
    "Cleaning",
    "Other",
)
COMPLAINT_STATUSES = ("Pending", "In Progress", "Resolved")

# Prototype storage only. Replace with a database repository in SHMS-18.
complaints = []

app = Flask(__name__)


@app.get("/")
def home():
    """Render the student form, warden table, and summary dashboard."""
    status_counts = {
        status: sum(1 for complaint in complaints if complaint["status"] == status)
        for status in COMPLAINT_STATUSES
    }
    return render_template(
        "index.html",
        complaints=complaints,
        categories=COMPLAINT_CATEGORIES,
        statuses=COMPLAINT_STATUSES,
        total=len(complaints),
        pending=status_counts["Pending"],
        progress=status_counts["In Progress"],
        resolved=status_counts["Resolved"],
    )


@app.post("/submit")
def submit():
    """Validate and register a complaint."""
    student = request.form.get("student", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()

    if not student or not category or not description:
        abort(400, description="Please fill all fields.")

    if category not in COMPLAINT_CATEGORIES:
        abort(400, description="Please select a valid complaint category.")

    complaints.append(
        {
            "student": student,
            "category": category,
            "description": description,
            "status": "Pending",
        }
    )
    return redirect(url_for("home"))


@app.post("/update/<int:index>")
def update(index):
    """Update a complaint status using the prototype's list index."""
    if index < 0 or index >= len(complaints):
        abort(404, description="Complaint not found.")

    new_status = request.form.get("status", "")
    if new_status not in COMPLAINT_STATUSES:
        abort(400, description="Please select a valid complaint status.")

    complaints[index]["status"] = new_status
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Local development entry point. Colab uses the separate iframe snippet
    # documented in README.md. Do not enable Flask debug mode in shared demos.
    app.run(host="127.0.0.1", port=5000, debug=False)
