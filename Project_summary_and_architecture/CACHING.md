# Redis Caching Implementation

## Overview
This project now includes Redis caching to optimize performance for frequent queries. Caching significantly reduces database load and improves response times for repeated queries.

## Configuration

### Environment Variables
Add the following to your `.env` file:

```env
REDIS_HOST=redis-15597.c82.us-east-1-2.ec2.cloud.redislabs.com
REDIS_PORT=15597
REDIS_PASSWORD=your_redis_password_here
REDIS_DB=0
```

### Installation
Install the Redis dependency:
```bash
pip install redis>=5.0.0
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

## Features

### Automatic Query Caching
The following queries are automatically cached:
- **Movie Title Search** - TTL: 30 minutes (1800s)
- **Director Search** - TTL: 1 hour (3600s)
- **Top Rated Movies** - TTL: 1 hour (3600s)
- **Genre Search** - TTL: 1 hour (3600s)
- **Actor Search** - TTL: 1 hour (3600s)

### Cache Management API Endpoints

#### Get Cache Statistics
```bash
GET /api/cache/stats
```

Returns:
```json
{
  "enabled": true,
  "connected": true,
  "keys_count": 42,
  "used_memory": "1.23M",
  "hits": 1500,
  "misses": 200,
  "hit_rate": 88.24
}
```

#### Clear Cache
```bash
DELETE /api/cache/clear?pattern=movie_cache:*
```

Returns:
```json
{
  "message": "Cache cleared successfully",
  "keys_deleted": 42,
  "pattern": "movie_cache:*"
}
```

#### Health Check (includes cache status)
```bash
GET /api/health
```

Returns:
```json
{
  "status": "healthy",
  "database": "connected",
  "agent": "ready",
  "cache": {
    "enabled": true,
    "connected": true,
    "keys_count": 42
  }
}
```

## How It Works

### Cache Key Generation
Each query generates a unique cache key based on:
- Function name/prefix
- Function arguments
- Query parameters

Example: `movie_cache:search_title:a3d5e9f2c1b4d8a7`

### Caching Flow
1. **Request received** → Check cache for existing result
2. **Cache HIT** → Return cached result (fast!)
3. **Cache MISS** → Query database → Store in cache → Return result

### Fallback Behavior
If Redis is unavailable:
- Caching is automatically disabled
- Application continues to work normally
- All queries go directly to MongoDB
- Warning logged: "⚠️ Redis connection failed. Caching disabled."

## Benefits

### Performance Improvements
- **Faster Response Times**: Cached queries return in < 10ms vs 100-500ms database queries
- **Reduced Database Load**: Frequently requested data served from cache
- **Cost Savings**: Fewer database operations reduce infrastructure costs

### Scalability
- Handles high traffic with minimal database impact
- Distributed cache shared across multiple API instances
- TTL ensures data freshness

## Cache Monitoring

### Check Cache Performance
```bash
curl http://localhost:8000/api/cache/stats
```

### View Logs
The application logs cache operations:
- `🎯 Cache HIT` - Result served from cache
- `❌ Cache MISS` - Query executed against database
- `💾 Cache SET` - Result stored in cache
- `🗑️ Cache DELETE` - Cache entry removed

## Troubleshooting

### Cache Not Working
1. Check Redis connection:
   ```bash
   redis-cli -h redis-15597.c82.us-east-1-2.ec2.cloud.redislabs.com -p 15597 -a your_password ping
   ```

2. Verify environment variables in `.env`

3. Check application logs for Redis connection errors

### Clear Specific Cache
To clear cache for specific queries:
```bash
# Clear all title searches
curl -X DELETE "http://localhost:8000/api/cache/clear?pattern=movie_cache:search_title:*"

# Clear all director searches
curl -X DELETE "http://localhost:8000/api/cache/clear?pattern=movie_cache:director:*"

# Clear everything
curl -X DELETE "http://localhost:8000/api/cache/clear?pattern=movie_cache:*"
```

## Code Examples

### Using Cache Decorator
```python
from cache import cache_result

@cache_result(ttl=3600, key_prefix="custom_query")
def my_query_function(self, param: str) -> str:
    # Your query logic here
    return result
```

### Manual Cache Operations
```python
from cache import get_cache

cache = get_cache()

# Set a value
cache.set("my_key", {"data": "value"}, ttl=600)

# Get a value
result = cache.get("my_key")

# Delete a value
cache.delete("my_key")

# Clear pattern
cache.clear_pattern("my_prefix:*")
```

## Security Notes

- Store Redis password in `.env` file
- Never commit `.env` to version control
- Use Redis AUTH for production
- Consider SSL/TLS for Redis connections in production
- Rotate credentials regularly

## Production Recommendations

1. **Use Redis Cluster** for high availability
2. **Monitor Cache Hit Rate** - aim for > 80%
3. **Adjust TTL** based on data update frequency
4. **Set Memory Limits** on Redis instance
5. **Enable Redis Persistence** (AOF or RDB)
6. **Use Connection Pooling** for better performance

## Related Files
- `cache.py` - Redis cache implementation
- `agent.py` - Database tools with caching decorators
- `api.py` - API endpoints with cache management
- `requirements.txt` - Python dependencies including redis
