# Architecture

## Current application

The application uses Flask routes, Jinja templates, and SQLite for durable complaint storage.

```text
Student / Warden browser
       |
       | GET /, POST /submit, POST /update/<complaint_id>
       v
Flask application (app.py)
       |
       | parameterized SQL queries
       v
SQLite database (instance/complaints.sqlite3)
       |
       | complaint rows and status counts
       v
Jinja template (templates/index.html)
       |
       v
Dashboard and complaint forms
```

## Key routes

| Route | Method | Purpose |
|---|---|---|
| / | GET | Show dashboard, complaint form, and warden table |
| /submit | POST | Validate and persist a complaint |
| /update/<complaint_id> | POST | Validate and persist a complaint status update |

## Data model

The `complaints` table contains:
- `id`: auto-incrementing primary key.
- `student`: required student name.
- `category`: required category constrained to the approved list.
- `description`: required complaint text.
- `status`: Pending, In Progress, or Resolved.
- `created_at`: SQLite timestamp at insertion.

Each Flask application context uses a request-scoped SQLite connection, closed during teardown. SQL statements use bound parameters for user input.

## Planned architecture

Future work may add:
- A users table and secure authentication.
- Role-based authorization for warden-only functions.
- Staff records and complaint assignment.
- An optional AI service that suggests category/priority for human review.

These features are not part of the SQLite persistence change until their implementation is merged and verified.
