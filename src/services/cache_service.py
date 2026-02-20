import json

class CacheService:
    def __init__(self, redis_client, ttl: int):
        self.redis = redis_client
        self.ttl = ttl

    async def get_or_set(self, key: str, compute_func):
        cached = await self.redis.get(key)
        if cached:
            return json.loads(cached)

        data = await compute_func()
        await self.redis.setex(key, self.ttl, json.dumps(data))
        return data
