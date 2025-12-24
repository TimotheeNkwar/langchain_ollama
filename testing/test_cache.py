"""
Test script for Redis caching functionality
Run this to verify cache is working correctly
"""

from cache import RedisCache, get_cache
import json
import time

def test_cache_connection():
    """Test basic Redis connection"""
    print("🔌 Testing Redis connection...")
    cache = RedisCache()
    
    if cache.enabled:
        print("✅ Redis connected successfully!")
        print(f"   Host: {cache.client.connection_pool.connection_kwargs.get('host')}")
        print(f"   Port: {cache.client.connection_pool.connection_kwargs.get('port')}")
        return cache
    else:
        print("❌ Redis connection failed - caching disabled")
        return None

def test_basic_operations(cache):
    """Test basic cache operations"""
    if not cache or not cache.enabled:
        print("⚠️ Skipping operations test - cache not available")
        return
    
    print("\n📝 Testing basic cache operations...")
    
    # Test SET
    test_data = {"movie": "The Matrix", "year": 1999, "rating": 8.7}
    cache.set("test_key", test_data, ttl=60)
    print("✅ SET operation successful")
    
    # Test GET
    result = cache.get("test_key")
    if result == test_data:
        print("✅ GET operation successful")
    else:
        print("❌ GET operation failed")
    
    # Test DELETE
    cache.delete("test_key")
    result = cache.get("test_key")
    if result is None:
        print("✅ DELETE operation successful")
    else:
        print("❌ DELETE operation failed")

def test_cache_performance(cache):
    """Test cache performance improvement"""
    if not cache or not cache.enabled:
        print("⚠️ Skipping performance test - cache not available")
        return
    
    print("\n⚡ Testing cache performance...")
    
    # Simulate expensive operation
    test_data = {"results": [f"movie_{i}" for i in range(100)]}
    
    # First call - cache miss
    start = time.time()
    cache.set("perf_test", test_data, ttl=60)
    result1 = cache.get("perf_test")
    time_uncached = time.time() - start
    
    # Second call - cache hit
    start = time.time()
    result2 = cache.get("perf_test")
    time_cached = time.time() - start
    
    print(f"   Uncached: {time_uncached*1000:.2f}ms")
    print(f"   Cached:   {time_cached*1000:.2f}ms")
    
    if time_cached < time_uncached:
        speedup = time_uncached / time_cached
        print(f"✅ Cache {speedup:.1f}x faster!")
    
    # Cleanup
    cache.delete("perf_test")

def test_cache_stats(cache):
    """Test cache statistics"""
    if not cache or not cache.enabled:
        print("⚠️ Skipping stats test - cache not available")
        return
    
    print("\n📊 Cache Statistics:")
    stats = cache.get_stats()
    print(json.dumps(stats, indent=2))

def test_pattern_clear(cache):
    """Test pattern-based cache clearing"""
    if not cache or not cache.enabled:
        print("⚠️ Skipping pattern clear test - cache not available")
        return
    
    print("\n🧹 Testing pattern-based clearing...")
    
    # Set multiple keys
    cache.set("test:1", "data1", ttl=60)
    cache.set("test:2", "data2", ttl=60)
    cache.set("test:3", "data3", ttl=60)
    cache.set("other:1", "data4", ttl=60)
    
    # Clear only test: pattern
    count = cache.clear_pattern("test:*")
    print(f"✅ Cleared {count} keys matching 'test:*'")
    
    # Verify
    if cache.get("test:1") is None and cache.get("other:1") is not None:
        print("✅ Pattern clearing works correctly")
    else:
        print("❌ Pattern clearing failed")
    
    # Cleanup
    cache.delete("other:1")

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Redis Cache Test Suite")
    print("="*60)
    
    cache = test_cache_connection()
    test_basic_operations(cache)
    test_cache_performance(cache)
    test_cache_stats(cache)
    test_pattern_clear(cache)
    
    print("\n" + "="*60)
    print("✨ Cache testing complete!")
    print("="*60)
    
    if cache:
        cache.close()

if __name__ == "__main__":
    main()
