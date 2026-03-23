import pytest
from fastapi.testclient import TestClient
from src.app import app

# Arrange: create a test client fixture
@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities(client):
    # Arrange is handled by the fixture
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act: sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Act: unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert unregister_resp.status_code == 200
    assert f"Removed {email}" in unregister_resp.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in seed data
    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
