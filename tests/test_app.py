import pytest

from app import app, complaints


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    complaints.clear()
    with app.test_client() as test_client:
        yield test_client
    complaints.clear()


def test_dashboard_shows_empty_state(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"No complaints registered yet." in response.data
    assert b"Total Complaints" in response.data


def test_valid_complaint_is_registered_as_pending(client):
    response = client.post(
        "/submit",
        data={
            "student": "Asha",
            "category": "Plumbing",
            "description": "Bathroom tap is leaking.",
        },
    )

    assert response.status_code == 302
    assert len(complaints) == 1
    assert complaints[0]["student"] == "Asha"
    assert complaints[0]["status"] == "Pending"

    dashboard = client.get("/")
    assert b"Bathroom tap is leaking." in dashboard.data
    assert b"Total Complaints" in dashboard.data


@pytest.mark.parametrize(
    "field",
    ["student", "category", "description"],
)
def test_missing_required_field_is_rejected(client, field):
    data = {
        "student": "Asha",
        "category": "Plumbing",
        "description": "Water leak",
    }
    data[field] = ""

    response = client.post("/submit", data=data)
    assert response.status_code == 400
    assert complaints == []


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
    assert complaints == []


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
    assert complaints == []


def test_status_can_be_updated(client):
    complaints.append(
        {
            "student": "Asha",
            "category": "Plumbing",
            "description": "Water leak",
            "status": "Pending",
        }
    )

    response = client.post("/update/0", data={"status": "In Progress"})
    assert response.status_code == 302
    assert complaints[0]["status"] == "In Progress"


def test_invalid_status_is_rejected(client):
    complaints.append(
        {
            "student": "Asha",
            "category": "Plumbing",
            "description": "Water leak",
            "status": "Pending",
        }
    )

    response = client.post("/update/0", data={"status": "Closed"})
    assert response.status_code == 400
    assert complaints[0]["status"] == "Pending"


def test_unknown_complaint_index_returns_404(client):
    response = client.post("/update/99", data={"status": "Resolved"})
    assert response.status_code == 404
