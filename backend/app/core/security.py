"""Rate limiting and client-IP helpers."""

import time
from collections import defaultdict, deque
from functools import lru_cache

from fastapi import Request

from app.core.config import get_settings
from app.core.errors import RateLimitExceededError


class SlidingWindowRateLimiter:
    """In-memory per-key limiter.

    State is per process, so with N workers the effective limit is N x max_requests.
    Use a shared store (e.g. Redis) or a reverse-proxy limit if that matters.
    """

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> int | None:
        """Record a hit. Returns None if allowed, else seconds until retry."""
        now = time.monotonic()
        hits = self._hits[key]
        while hits and now - hits[0] >= self.window_seconds:
            hits.popleft()
        if len(hits) >= self.max_requests:
            return max(1, int(self.window_seconds - (now - hits[0])) + 1)
        hits.append(now)
        self._prune(now)
        return None

    def _prune(self, now: float) -> None:
        """Drop idle keys so memory stays bounded."""
        if len(self._hits) < 1024:
            return
        for key in [k for k, v in self._hits.items() if not v or now - v[-1] >= self.window_seconds]:
            del self._hits[key]

    def reset(self) -> None:
        self._hits.clear()


@lru_cache
def get_contact_rate_limiter() -> SlidingWindowRateLimiter:
    settings = get_settings()
    return SlidingWindowRateLimiter(
        settings.contact_rate_limit_max_requests, settings.contact_rate_limit_window_seconds
    )


def get_client_ip(request: Request) -> str:
    """Client IP. X-Forwarded-For is honoured only when explicitly trusted."""
    if get_settings().trust_proxy_headers:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            # The last entry is the one appended by our (single) trusted proxy.
            return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


async def contact_rate_limit(request: Request) -> None:
    """FastAPI dependency for POST /contact."""
    retry_after = get_contact_rate_limiter().check(get_client_ip(request))
    if retry_after is not None:
        raise RateLimitExceededError(headers={"Retry-After": str(retry_after)})
