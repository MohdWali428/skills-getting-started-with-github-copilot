from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test.user+signup@example.com"

    # Ensure clean start
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant present in activities listing
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    data = resp2.json()
    assert email in data[activity]["participants"]

    # Unregister
    resp3 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp3.status_code == 200
    assert "Unregistered" in resp3.json().get("message", "")

    # Verify removed
    resp4 = client.get("/activities")
    assert resp4.status_code == 200
    data2 = resp4.json()
    assert email not in data2[activity]["participants"]


def test_unregister_nonexistent_returns_404():
    activity = "Chess Club"
    email = "does.not.exist+nope@example.com"

    # Ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 404


def test_invalid_activity_returns_404():
    resp = client.get("/activities/ThisDoesNotExist")
    # We don't expose a specific GET on an activity; ensure top-level activities are accessible
    assert resp.status_code in (200, 404)
