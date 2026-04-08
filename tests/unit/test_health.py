"""Smoke test to verify project setup works."""


def test_health_endpoint(client):
    """Test that the health check endpoint responds correctly."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "energy-audit-backend"
