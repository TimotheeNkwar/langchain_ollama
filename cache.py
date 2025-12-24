"""
Redis caching utility for frequent query optimization
Provides caching layer for movie database queries
"""

import redis
import json
import hashlib
from typing import Optional, Any
from functools import wraps
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

class RedisCache:
    """Redis cache manager for movie queries"""
    
    def __init__(self):
        """Initialize Redis connection"""
        redis_host = os.getenv('REDIS_HOST', 'redis-15597.c82.us-east-1-2.ec2.cloud.redislabs.com')
        redis_port = int(os.getenv('REDIS_PORT', '15597'))
        redis_password = os.getenv('REDIS_PASSWORD', '')
        redis_db = int(os.getenv('REDIS_DB', '0'))
        
        try:
            self.client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password if redis_password else None,
                db=redis_db,
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Test connection
            self.client.ping()
            self.enabled = True
            logger.info(f"✅ Redis cache connected: {redis_host}:{redis_port}")
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed: {e}. Caching disabled.")
            self.client = None
            self.enabled = False
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a unique cache key from function arguments"""
        # Create a unique identifier from arguments
        key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
        # Hash for consistent key length
        key_hash = hashlib.md5(key_data.encode()).hexdigest()
        return f"movie_cache:{prefix}:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled or not self.client:
            return None
        
        try:
            value = self.client.get(key)
            if value:
                logger.debug(f"🎯 Cache HIT: {key}")
                return json.loads(value)
            logger.debug(f"❌ Cache MISS: {key}")
            return None
        except Exception as e:
            logger.warning(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL (default 1 hour)"""
        if not self.enabled or not self.client:
            return False
        
        try:
            serialized = json.dumps(value, default=str)
            self.client.setex(key, ttl, serialized)
            logger.debug(f"💾 Cache SET: {key} (TTL: {ttl}s)")
            return True
        except Exception as e:
            logger.warning(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete a key from cache"""
        if not self.enabled or not self.client:
            return False
        
        try:
            self.client.delete(key)
            logger.debug(f"🗑️ Cache DELETE: {key}")
            return True
        except Exception as e:
            logger.warning(f"Cache delete error: {e}")
            return False
    
    def clear_pattern(self, pattern: str = "movie_cache:*") -> int:
        """Clear all keys matching a pattern"""
        if not self.enabled or not self.client:
            return 0
        
        try:
            keys = self.client.keys(pattern)
            if keys:
                count = self.client.delete(*keys)
                logger.info(f"🧹 Cleared {count} cache entries matching '{pattern}'")
                return count
            return 0
        except Exception as e:
            logger.warning(f"Cache clear error: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """Get cache statistics"""
        if not self.enabled or not self.client:
            return {"enabled": False}
        
        try:
            info = self.client.info()
            keys_count = len(self.client.keys("movie_cache:*"))
            return {
                "enabled": True,
                "connected": True,
                "keys_count": keys_count,
                "used_memory": info.get('used_memory_human', 'N/A'),
                "hits": info.get('keyspace_hits', 0),
                "misses": info.get('keyspace_misses', 0),
                "hit_rate": round(
                    info.get('keyspace_hits', 0) / 
                    max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0), 1) * 100, 
                    2
                )
            }
        except Exception as e:
            logger.warning(f"Cache stats error: {e}")
            return {"enabled": True, "connected": False, "error": str(e)}
    
    def close(self):
        """Close Redis connection"""
        if self.client:
            try:
                self.client.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.warning(f"Error closing Redis: {e}")


def cache_result(ttl: int = 3600, key_prefix: str = "query"):
    """
    Decorator to cache function results in Redis
    
    Args:
        ttl: Time to live in seconds (default 1 hour)
        key_prefix: Prefix for cache key
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get cache instance from self if available
            cache = getattr(self, 'cache', None)
            if not cache or not cache.enabled:
                return func(self, *args, **kwargs)
            
            # Generate cache key
            cache_key = cache._generate_key(key_prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = func(self, *args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator


# Global cache instance
_cache_instance = None

def get_cache() -> RedisCache:
    """Get or create the global cache instance"""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = RedisCache()
    return _cache_instance
