from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_succes():
    response = client.post(
        "/api/register",
        json={
            "username": "akeoneuefo",
            "password": "superone",
            "name": "akeoneufo",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"data": "ok"}
