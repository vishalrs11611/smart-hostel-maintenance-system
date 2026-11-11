import pytest

from app import app, get_db


@pytest.fixture()
def client(tmp_path):
    database_path = tmp_path / "test-complaints.sqlite3"
    app.config.update(TESTING=True, DATABASE=str(database_path))
    with app.test_client() as test_client:
        yield test_client


def fetch_complaints():
    with app.app_context():
        return get_db().execute(
            """
            SELECT id, student, category, description, status
            FROM complaints
            ORDER BY id
            """
        ).fetchall()


def register_complaint(client, student="Asha", description="Water leak"):
    return client.post(
        "/submit",
        data={
            "student": student,
            "category": "Plumbing",
            "description": description,
        },
    )


def test_dashboard_shows_empty_state(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No complaints registered yet." in response.data
    assert b"Total Complaints" in response.data


def test_valid_complaint_is_registered_as_pending(client):
    response = register_complaint(
        client, description="Bathroom tap is leaking."
    )

    assert response.status_code == 302
    rows = fetch_complaints()
    assert len(rows) == 1
    assert rows[0]["student"] == "Asha"
    assert rows[0]["status"] == "Pending"

    dashboard = client.get("/")
    assert b"Bathroom tap is leaking." in dashboard.data
    assert b"Total Complaints" in dashboard.data


@pytest.mark.parametrize("field", ["student", "category", "description"])
def test_missing_required_field_is_rejected(client, field):
    data = {
        "student": "Asha",
        "category": "Plumbing",
        "description": "Water leak",
    }
    data[field] = ""

    response = client.post("/submit", data=data)
    assert response.status_code == 400
    assert fetch_complaints() == []


def test_whitespace_only_text_is_rejected(client):
    response = client.post(
        "/submit",
        data={
            "student": "   ",
            "category": "Plumbing",
            "description": "Water leak",
        },
    )
    assert response.status_code == 400
    assert fetch_complaints() == []


def test_unknown_category_is_rejected(client):
    response = client.post(
        "/submit",
        data={
            "student": "Asha",
            "category": "Unlisted category",
            "description": "Water leak",
        },
    )
    assert response.status_code == 400
    assert fetch_complaints() == []


def test_status_can_be_updated(client):
    register_complaint(client)
    complaint_id = fetch_complaints()[0]["id"]

    response = client.post(
        f"/update/{complaint_id}", data={"status": "In Progress"}
    )
    assert response.status_code == 302
    assert fetch_complaints()[0]["status"] == "In Progress"


def test_invalid_status_is_rejected(client):
    register_complaint(client)
    complaint_id = fetch_complaints()[0]["id"]

    response = client.post(
        f"/update/{complaint_id}", data={"status": "Closed"}
    )
    assert response.status_code == 400
    assert fetch_complaints()[0]["status"] == "Pending"


def test_unknown_complaint_id_returns_404(client):
    response = client.post("/update/9999", data={"status": "Resolved"})
    assert response.status_code == 404


def test_complaint_persists_across_independent_requests(client):
    register_complaint(client, student="Nikhil", description="No water supply")

    # A new request gets a new Flask application context and DB connection.
    response = client.get("/")
    assert response.status_code == 200
    assert b"Nikhil" in response.data
    assert b"No water supply" in response.data
    assert len(fetch_complaints()) == 1


def test_dashboard_counts_match_database_records(client):
    register_complaint(client, student="Asha", description="Tap leak")
    register_complaint(client, student="Ravi", description="Broken light")

    second_id = fetch_complaints()[1]["id"]
    client.post(f"/update/{second_id}", data={"status": "Resolved"})

    dashboard = client.get("/")
    assert b"<h3>2</h3>" in dashboard.data
    assert b"<h3>1</h3>" in dashboard.data
    assert b"Resolved" in dashboard.data
