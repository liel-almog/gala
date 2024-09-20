from fastapi.testclient import TestClient
from app.core.app import app


def test_read_main():
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == "Health"
