from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static():
    # Arrange: nothing special, client already available

    # Act
    response = client.get("/")

    # Assert: should redirect to /static/index.html
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_list():
    # Arrange: nothing to prepare

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data  # known activity should exist


def test_signup_and_unregistration():
    test_email = "test@student.com"

    # Arrange: ensure clean state for the Chess Club activity
    if test_email in activities["Chess Club"]["participants"]:
        activities["Chess Club"]["participants"].remove(test_email)

    # Act & Assert: sign up works
    resp = client.post("/activities/Chess%20Club/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email in activities["Chess Club"]["participants"]

    # Act & Assert: duplicate signup fails
    dup = client.post("/activities/Chess%20Club/signup", params={"email": test_email})
    assert dup.status_code == 400

    # Act & Assert: unregister succeeds
    unreg = client.post("/activities/Chess%20Club/unregister", params={"email": test_email})
    assert unreg.status_code == 200
    assert test_email not in activities["Chess Club"]["participants"]

    # Act & Assert: unregistering again yields error
    bad = client.post("/activities/Chess%20Club/unregister", params={"email": test_email})
    assert bad.status_code == 400
