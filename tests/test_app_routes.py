from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_root_redirect_to_static_index():
    # Do not follow redirects so we can assert the redirect location
    res = client.get("/", follow_redirects=False)
    assert res.status_code in (301, 302, 307, 308)
    assert res.headers["location"] == "/static/index.html"


def test_get_static_index_contains_site_title():
    res = client.get("/static/index.html")
    assert res.status_code == 200
    assert "Mergington High School" in res.text


def test_signup_nonexistent_activity_returns_404():
    res = client.post("/activities/NoSuchActivity/signup?email=ghost@mergington.edu")
    assert res.status_code == 404
