import random
import asyncio
from src.config.settings import EXTERNAL_SERVICE_FAILURE_RATE


async def fetch_external_data():
    await asyncio.sleep(0.05)  # simulate latency
    if random.random() < EXTERNAL_SERVICE_FAILURE_RATE:
        raise RuntimeError("Simulated external service failure")
    return {"external": "ok", "value": random.randint(100, 200)}
