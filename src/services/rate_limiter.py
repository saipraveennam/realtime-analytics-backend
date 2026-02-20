class RateLimiter:
    def __init__(self, redis_client, limit: int, window: int):
        self.redis = redis_client
        self.limit = limit
        self.window = window

    async def allow(self, client_id: str):
        key = f"rate:{client_id}"
        count = await self.redis.incr(key)

        if count == 1:
            await self.redis.expire(key, self.window)

        if count > self.limit:
            ttl = await self.redis.ttl(key)
            return False, ttl

        return True, None
