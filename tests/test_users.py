import pytest
from jose import jwt
from app.schemas import UserResponse, Token
from app.config import settings


def test_root(client):
    res = client.get(
        "/",
    )
    assert res.json().get("message") == "Hello, World!"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "pavel@gmail.com", "password": "pass123"}
    )
    new_user = UserResponse(**res.json())
    assert new_user.email == "pavel@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user: dict):
    res = client.post(
        "/login/",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("pavel@gmail.com", "bullshit", 403),
        ("pavel1@gmail.com", "pass123", 403),
        ("bullshit@gmail.com", None, 422),
        (None, "bullshit", 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
