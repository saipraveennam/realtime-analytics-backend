from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis.asyncio as redis

from src.api import metrics
from src.services.rate_limiter import RateLimiter
from src.services.circuit_breaker import CircuitBreaker
from src.services.external_service import fetch_external_data
from src.services.cache_service import CacheService
from src.config.settings import *


app = FastAPI(title="Real-Time Analytics Backend")

# Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

# Services
rate_limiter = RateLimiter(redis_client, RATE_LIMIT, RATE_WINDOW)
circuit_breaker = CircuitBreaker(CB_FAILURE_THRESHOLD, CB_RESET_TIMEOUT)
cache_service = CacheService(redis_client, CACHE_TTL)

# Inject cache into metrics module
metrics.cache_service = cache_service


@app.get("/health")
async def health():
    await redis_client.ping()
    return {"status": "ok"}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path == "/api/metrics" and request.method == "POST":
        allowed, retry = await rate_limiter.allow(request.client.host)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests"},
                headers={"Retry-After": str(retry)},
            )

    return await call_next(request)


@app.get("/external")
async def external_call():
    return await circuit_breaker.call(fetch_external_data)


app.include_router(metrics.router, prefix="/api")
