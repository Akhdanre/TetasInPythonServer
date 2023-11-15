from fastapi.testclient import TestClient
from app.main import app
from app.service.user_service import User

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
    assert response.json() == {"data": "ok", "errors": None}


def test_register_duplicate():
    User.deleteAllUsers()

    responseSample = client.post(
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


def test_update_user():
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
            "username": "akeoneuefo",
            "password": "superone"
        }
    )
    res = response.json()
    data = res["data"]
    responseUpdate = client.patch(
        "/api/user/update",
        headers={
            "X-API-TOKEN": data["token"]
        },
        json={
            "password": "loremipse",
            "name": "akeon de supo"
        }
    )

    assert responseUpdate.status_code == 200
