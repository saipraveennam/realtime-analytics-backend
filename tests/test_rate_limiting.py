import requests

BASE_URL = "http://localhost:8000"

def test_rate_limit_exceeded():
    payload = {
        "timestamp": "2025-01-01T10:00:00",
        "value": 1,
        "type": "cpu"
    }

    last_response = None
    for _ in range(7):  # exceed limit
        last_response = requests.post(
            f"{BASE_URL}/api/metrics",
            json=payload
        )

    assert last_response.status_code == 429
    assert "Retry-After" in last_response.headers
