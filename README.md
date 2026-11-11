# Smart Hostel Maintenance System

A Flask-based hostel complaint management application developed as a mini-project case study for **AI-Driven Software Engineering & Project Management**.

## Features
- Student complaint registration with category and description.
- Server-side validation of required fields and allowed categories.
- Warden dashboard listing submitted complaints.
- Complaint status updates: Pending, In Progress, and Resolved.
- Dashboard counts for total and status-wise complaints.
- SQLite persistence for complaint records.

## Technology
- Python 3.10+
- Flask
- SQLite (Python standard library)
- Jinja templates
- pytest for automated tests
- GitHub Actions for continuous integration

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000.

By default, SQLite creates `instance/complaints.sqlite3`. Set `SHMS_DATABASE` to use a different database path.

## Run tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

The test suite uses a temporary SQLite database and does not touch the local application database.

## Run in Google Colab

Clone or upload this repository, install its requirements, and run this in a notebook cell:

```python
import socket
import threading
import time
from google.colab import output
from app import app

sock = socket.socket()
sock.bind(("0.0.0.0", 0))
port = sock.getsockname()[1]
sock.close()

threading.Thread(
    target=lambda: app.run(
        host="0.0.0.0", port=port, debug=False,
        use_reloader=False, threaded=True
    ),
    daemon=True,
).start()

for _ in range(50):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            break
    except OSError:
        time.sleep(0.2)
else:
    raise RuntimeError("Flask did not start")

output.serve_kernel_port_as_iframe(
    port, path="/", width="100%", height=800
)
```

For a persistent demo in Colab, set `app.config["DATABASE"]` to a path in the mounted Google Drive before the first request. The default Colab filesystem is temporary.

## Current limitations and planned enhancements
Student/warden authentication, role-based authorization, maintenance-staff assignment, and a runtime AI classifier are not implemented yet. These remain planned enhancements in Jira. The AI case-study log distinguishes AI assistance used during engineering from AI functionality included in the application.

## Project management
Jira project: [SHMS - Smart Hostel Maintenance System](https://vishalrs11611.atlassian.net/jira/software/projects/SHMS/summary)

Use Jira issue keys in branch names and commit messages (for example, `SHMS-18-sqlite-persistence` and `SHMS-18 Persist complaints in SQLite`).

## Documentation
- [Requirements baseline](docs/requirements.md)
- [Architecture](docs/architecture.md)
- [Test cases](docs/test-cases.md)
- [AI usage log](docs/ai-usage-log.md)
- [Case study plan](docs/case-study-plan.md)
