from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "johndoe", "email": "john.doe@example.com", "full_name": "John Doe", "route": "Main St"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
    assert response.json()["email"] == "john.doe@example.com"
    assert response.json()["full_name"] == "John Doe"
    assert response.json()["route"] == "Main St"


def test_read_user():
    response = client.get("/users/johndoe")
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
    assert response.json()["email"] == "john.doe@example.com"
    assert response.json()["full_name"] == "John Doe"
    assert response.json()["route"] == "Main St"


def test_update_user():
    response = client.put(
        "/users/johndoe",
        json={"username": "johndoe", "email": "john.doe.updated@example.com", "full_name": "John Doe Updated", "route": "Elm St"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "johndoe"
    assert response.json()["email"] == "john.doe.updated@example.com"
    assert response.json()["full_name"] == "John Doe Updated"
    assert response.json()["route"] == "Elm St"


def test_delete_user():
    response = client.delete("/users/johndoe")
    assert response.status_code == 200
    assert response.json() == {"message": "User johndoe deleted successfully"}


def test_create_user_with_street1():
    response = client.post(
        "/users/",
        json={"username": "janedoe", "email": "jane.doe@example.com", "full_name": "Jane Doe", "street1": "123 Main St", "route": "Oak Ave"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"
    assert response.json()["email"] == "jane.doe@example.com"
    assert response.json()["full_name"] == "Jane Doe"
    assert response.json()["street1"] == "123 Main St"
    assert response.json()["route"] == "Oak Ave"


def test_read_user_with_street1():
    response = client.get("/users/janedoe")
    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"
    assert response.json()["email"] == "jane.doe@example.com"
    assert response.json()["full_name"] == "Jane Doe"
    assert response.json()["street1"] == "123 Main St"
    assert response.json()["route"] == "Oak Ave"


def test_update_user_with_street1():
    response = client.put(
        "/users/janedoe",
        json={"username": "janedoe", "email": "jane.doe.updated@example.com", "full_name": "Jane Doe Updated", "street1": "456 Oak Ave", "route": "Pine Ln"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "janedoe"
    assert response.json()["email"] == "jane.doe.updated@example.com"
    assert response.json()["full_name"] == "Jane Doe Updated"
    assert response.json()["street1"] == "456 Oak Ave"
    assert response.json()["route"] == "Pine Ln"