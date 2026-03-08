from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static():
    response = client.get("/")
    # should redirect to /static/index.html
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_list():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # there should be at least one known activity
    assert "Chess Club" in data


def test_signup_and_unregistration():
    test_email = "test@student.com"
    # start with clean state: ensure not in participants already
    if test_email in activities["Chess Club"]["participants"]:
        activities["Chess Club"]["participants"].remove(test_email)

    # sign up
    resp = client.post("/activities/Chess%20Club/signup", params={"email": test_email})
    assert resp.status_code == 200
    assert test_email in activities["Chess Club"]["participants"]

    # duplicate signup should fail
    dup = client.post("/activities/Chess%20Club/signup", params={"email": test_email})
    assert dup.status_code == 400

    # unregister
    unreg = client.post("/activities/Chess%20Club/unregister", params={"email": test_email})
    assert unreg.status_code == 200
    assert test_email not in activities["Chess Club"]["participants"]

    # unregister again should fail
    bad = client.post("/activities/Chess%20Club/unregister", params={"email": test_email})
    assert bad.status_code == 400
