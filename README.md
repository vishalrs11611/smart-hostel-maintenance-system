# Smart Hostel Maintenance System

A Flask-based hostel complaint management prototype developed as a mini-project case study for **AI-Driven Software Engineering & Project Management**.

## Current baseline features
- Student complaint registration with category and description.
- Server-side validation of required fields and allowed categories.
- Warden dashboard listing submitted complaints.
- Complaint status updates: Pending, In Progress, and Resolved.
- Dashboard counts for total and status-wise complaints.

## Technology
- Python 3.10+
- Flask
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

## Run tests

```bash
pytest -q
```

## Run in Google Colab

Install the dependencies, then run this in a notebook cell after uploading/cloning the repository:

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

## Current limitations and planned enhancements
The prototype currently stores complaints in memory, so records disappear when the process restarts. It does not yet include a database, login, role-based access, maintenance-staff assignment, or an AI model in the running application. These are documented as planned enhancements in Jira and the `docs/` directory.

## Project management
Jira project: [SHMS - Smart Hostel Maintenance System](https://vishalrs11611.atlassian.net/jira/software/projects/SHMS/summary)

Use Jira issue keys in branch names and commit messages (for example, `SHMS-7-flask-project-structure` and `SHMS-7 Refactor Flask app`).

## Documentation
- [Requirements baseline](docs/requirements.md)
- [Architecture](docs/architecture.md)
- [Test cases](docs/test-cases.md)
- [AI usage log](docs/ai-usage-log.md)
- [Case study plan](docs/case-study-plan.md)

## Academic integrity and AI use
AI assistance is documented in `docs/ai-usage-log.md`. AI-generated code and test suggestions must be reviewed and verified by running tests. The application is not described as AI-powered unless an AI runtime feature is actually implemented and evaluated.
