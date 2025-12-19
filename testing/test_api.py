"""
Test script for the Movie AI Agent API (FastAPI)
Run this after starting the API server (uvicorn api:app --reload)
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Print a section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_home():
    """Test the home endpoint"""
    print_section("Testing Home Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_search_movies():
    """Test search movies by title"""
    print_section("Testing Search Movies")
    response = requests.get(f"{BASE_URL}/api/movies/search", params={"title": "batman"})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list) and len(data) > 0:
        print(f"Found {len(data)} movies")
        print(json.dumps(data[:2], indent=2))  # Show first 2
    else:
        print(json.dumps(data, indent=2))

def test_top_movies():
    """Test top rated movies"""
    print_section("Testing Top Rated Movies")
    response = requests.get(f"{BASE_URL}/api/movies/top", params={"limit": 5})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list):
        print(f"Top {len(data)} movies:")
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data, indent=2))

def test_movies_by_director():
    """Test movies by director"""
    print_section("Testing Movies by Director")
    response = requests.get(f"{BASE_URL}/api/movies/director", params={"name": "nolan"})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list):
        print(f"Found {len(data)} movies")
        print(json.dumps(data[:3], indent=2))
    else:
        print(json.dumps(data, indent=2))

def test_movies_by_genre():
    """Test movies by genre"""
    print_section("Testing Movies by Genre")
    response = requests.get(f"{BASE_URL}/api/movies/genre", params={"genre": "action"})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list):
        print(f"Found {len(data)} action movies")
        print(json.dumps(data[:3], indent=2))
    else:
        print(json.dumps(data, indent=2))

def test_movies_by_year_range():
    """Test movies by year range"""
    print_section("Testing Movies by Year Range")
    response = requests.get(f"{BASE_URL}/api/movies/year-range", params={"start": 1990, "end": 1995})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list):
        print(f"Found {len(data)} movies from 1990-1995")
        print(json.dumps(data[:3], indent=2))
    else:
        print(json.dumps(data, indent=2))

def test_movies_with_actor():
    """Test movies with actor"""
    print_section("Testing Movies with Actor")
    response = requests.get(f"{BASE_URL}/api/movies/actor", params={"name": "dicaprio"})
    print(f"Status: {response.status_code}")
    data = response.json()
    if isinstance(data, list):
        print(f"Found {len(data)} movies with DiCaprio")
        print(json.dumps(data[:3], indent=2))
    else:
        print(json.dumps(data, indent=2))

def test_statistics():
    """Test database statistics"""
    print_section("Testing Database Statistics")
    response = requests.get(f"{BASE_URL}/api/movies/statistics")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_query_agent():
    """Test natural language query"""
    print_section("Testing Natural Language Query")
    response = requests.post(
        f"{BASE_URL}/api/query",
        json={"question": "What are the top 3 Christopher Nolan movies?"}
    )
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_health():
    """Test health check"""
    print_section("Testing Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def main():
    """Run all tests"""
    print("\n" + "🎬"*30)
    print("  IMDB Movie AI Agent API Tests")
    print("🎬"*30)
    
    try:
        test_home()
        test_health()
        test_search_movies()
        test_top_movies()
        test_movies_by_director()
        test_movies_by_genre()
        test_movies_by_year_range()
        test_movies_with_actor()
        test_statistics()
        test_query_agent()
        
        print("\n" + "✅"*30)
        print("  All tests completed!")
        print("✅"*30 + "\n")
        
        print("\n❌ Error: Cannot connect to API")
        print("Make sure the API server is running:")
        print("  uvicorn api:app --reload --host 0.0.0.0 --port 8000\n")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}\n")

if __name__ == "__main__":
    main()
