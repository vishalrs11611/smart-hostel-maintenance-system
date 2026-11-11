# Architecture

## Current prototype

The application uses Flask routes, Jinja templates, and in-memory Python storage.

```text
Student browser
    |
    | POST /submit
    v
Flask application (app.py) ------> in-memory complaints list
    |                                  |
    | GET /                            |
    v                                  |
Jinja template (templates/index.html) <-
    |
    | POST /update/<index>
    v
Warden dashboard and status workflow
```

## Key routes

| Route | Method | Purpose |
|---|---|---|
| / | GET | Show dashboard, complaint form, and warden table |
| /submit | POST | Validate and register complaint |
| /update/<index> | POST | Validate and update a complaint status |

## Target architecture

The planned architecture introduces a persistent repository, authentication, and role checks:

- Flask routes handle HTTP requests and validation.
- Jinja templates render the interface.
- A SQLite data layer stores users and complaints.
- Authentication identifies the current user.
- Authorization limits warden actions.
- Optional AI service suggests category/priority; a human reviews the suggestion.

The target architecture is not yet implemented. It should be updated as each Jira enhancement is completed.
