from fastapi.testclient import TestClient
from fastapi import Depends
from app.main import app
from app.service.user_service import User
from sqlalchemy.orm import Session
from app.utils.deps import get_db


client = TestClient(app)


def test_register_succes():
    deleteStatus = User.deleteAllUsers()

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
