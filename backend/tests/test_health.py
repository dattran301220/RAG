from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Kiểm tra endpoint root '/' trả về thông tin chào mừng và docs"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data


def test_health_check_endpoint():
    """Kiểm tra endpoint '/api/v1/health' trả về cấu trúc trạng thái dịch vụ"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "database" in data["services"]
    assert "redis" in data["services"]
    assert "qdrant" in data["services"]
    assert "minio" in data["services"]
