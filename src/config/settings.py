import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

RATE_LIMIT = int(os.getenv("RATE_LIMIT", 5))        
RATE_WINDOW = int(os.getenv("RATE_WINDOW", 60))     

CACHE_TTL = int(os.getenv("CACHE_TTL", 300))        

CB_FAILURE_THRESHOLD = int(os.getenv("CB_FAILURE_THRESHOLD", 3))
CB_RESET_TIMEOUT = int(os.getenv("CB_RESET_TIMEOUT", 10))

EXTERNAL_SERVICE_FAILURE_RATE = float(
    os.getenv("EXTERNAL_SERVICE_FAILURE_RATE", 0.2)
)
