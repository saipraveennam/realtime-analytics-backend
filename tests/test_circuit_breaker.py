import os
import requests
import time

BASE_URL = "http://localhost:8000"

def test_circuit_breaker_fallback():
    # Force external service to fail
    os.environ["EXTERNAL_SERVICE_FAILURE_RATE"] = "1.0"

    fallback_seen = False

    for _ in range(15):
        r = requests.get(f"{BASE_URL}/external")
        if r.status_code == 200:
            data = r.json()
            if data.get("fallback") is True:
                fallback_seen = True
                break
        time.sleep(0.1)

    assert fallback_seen is True
