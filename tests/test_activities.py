from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_and_reflects_in_activity():
    email = "teststudent@mergington.edu"
    activity = "Chess Club"

    # Ensure not already signed up
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json()["message"]

    # Confirm participant appears
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]


def test_signup_duplicate_fails():
    email = "duplicate@mergington.edu"
    activity = "Programming Class"

    # First signup succeeds
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200

    # Second signup fails
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 400


def test_unregister_success_and_not_found():
    email = "toremove@mergington.edu"
    activity = "Chess Club"

    # Add participant to remove
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200

    # Remove participant
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert "Unregistered" in res.json()["message"]

    # Removing again should return 404
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 404
