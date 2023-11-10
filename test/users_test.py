from fastapi.testclient import TestClient
from fastapi import Depends
from app.main import app
from app.service.user_service import User
from sqlalchemy.orm import Session
from app.utils.deps import get_db


client = TestClient(app)


def test_register_succes():
    User.deleteAllUsers()

    response = client.post(
        "/api/user",
        json={
            "username": "akeoneuefo",
            "password": "superone",
            "name": "akeoneufo",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"data": "ok"}

def test_register_duplicate():
    User.deleteAllUsers()

    responseSample= client.post(
        "/api/user",
        json={
            "username": "akeoneuefo",
            "password": "superone",
            "name": "akeoneufo",
        },
    )

    response = client.post(
        "/api/user",
        json={
            "username": "akeoneuefo",
            "password": "superone",
            "name": "akeoneufo",
        },
    )

    assert response.status_code == 400


def test_register_failed():
    User.deleteAllUsers()

    response = client.post(
        "/api/user",
        json={
            "username": "",
            "password": "",
            "name": "",
        },
    )

    assert response.status_code == 400
        # assert response.json() == {"data": "ok"}
