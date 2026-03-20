import redis.asyncio as aioredis
import os


REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = aioredis.from_url(REDIS_URL, decode_responses=True)

async def blacklist_token(token: str, expires_in: int):
    """Store the token in Redis until it expires."""
    await redis.set(token, "blacklisted", ex=expires_in)

async def is_token_blacklisted(token: str) -> bool:
    return await redis.exists(token) > 0