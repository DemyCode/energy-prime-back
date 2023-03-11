from fastapi.testclient import TestClient

from energy_prime_back.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_user():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []
