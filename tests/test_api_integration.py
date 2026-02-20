import time
import requests

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_post_metric():
    payload = {
        "timestamp": "2025-01-01T10:00:00",
        "value": 50,
        "type": "cpu"
    }
    r = requests.post(f"{BASE_URL}/api/metrics", json=payload)
    assert r.status_code == 201


def test_summary_computation_and_cache():
    # First call (compute)
    r1 = requests.get(f"{BASE_URL}/api/metrics/summary?metric_type=cpu")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["count"] >= 1

    # Second call (should be cached)
    r2 = requests.get(f"{BASE_URL}/api/metrics/summary?metric_type=cpu")
    assert r2.status_code == 200
    data2 = r2.json()

    assert data1 == data2
