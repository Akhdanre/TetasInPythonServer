from fastapi.testclient import TestClient
from app.main import app
from app.service.user_service import User

client = TestClient(app)

def test_auth():
    User.deleteAllUsers()
    client.post(
        "/api/user",
        json={
            "username": "akeoneuefo",
            "password": "superone",
            "name": "akeoneufo",
        },
    )

    response = client.post(
        "/api/authentication",
        json={
            "username" : "akeoneuefo",
            "password" : "superone"
        }
    )

    assert response.status_code == 200