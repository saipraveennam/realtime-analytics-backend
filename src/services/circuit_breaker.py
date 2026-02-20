from enum import Enum
import time
import asyncio


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int, reset_timeout_seconds: int):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout_seconds
        self.lock = asyncio.Lock()

    async def call(self, func, *args, **kwargs):
        async with self.lock:
            now = time.time()

            # OPEN state → return fallback
            if self.state == CircuitState.OPEN:
                if now - self.last_failure_time > self.reset_timeout:
                    self.state = CircuitState.HALF_OPEN
                else:
                    return {
                        "fallback": True,
                        "reason": "circuit open"
                    }

            try:
                result = await func(*args, **kwargs)

                # Success path
                self.failure_count = 0
                self.state = CircuitState.CLOSED
                return result

            except Exception:
                self.failure_count += 1
                self.last_failure_time = now

                if self.failure_count >= self.failure_threshold:
                    self.state = CircuitState.OPEN

                return {
                    "fallback": True,
                    "reason": "external service failure"
                }
