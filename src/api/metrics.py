from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import List

from src.services.cache_service import CacheService
from src.config.settings import CACHE_TTL

router = APIRouter()
metrics_db: List[dict] = []

# Cache will be injected later
cache_service: CacheService = None

class Metric(BaseModel):
    timestamp: datetime
    value: float
    type: str

@router.post("/metrics", status_code=201)
async def create_metric(metric: Metric):
    metrics_db.append(metric.dict())

    
    if cache_service:
        cache_key = f"summary:{metric.type}"
        await cache_service.redis.delete(cache_key)

    return {"message": "Metric stored successfully"}

@router.get("/metrics/summary")
async def get_summary(metric_type: str):

    cache_key = f"summary:{metric_type}"

    async def compute_summary():
        values = [m["value"] for m in metrics_db if m["type"] == metric_type]
        if not values:
            return {"type": metric_type, "count": 0, "average": 0}

        return {
            "type": metric_type,
            "count": len(values),
            "average": sum(values) / len(values),
        }

    return await cache_service.get_or_set(cache_key, compute_summary)
