"""
FastAPI for IMDB Movie AI Agent
Provides REST endpoints to query the movie database
"""

from fastapi import FastAPI, Query, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import MovieAgent
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os
import json
from typing import Optional
from loguru import logger

# Configure loguru for api.py
logger.remove()  # Remove default handler
logger.add(
    "api.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    backtrace=True,
    diagnose=True
)
logger.add(
    lambda msg: print(msg, end=''),
    level="INFO",
    format="{message}",
    colorize=True
)

# Load environment variables
load_dotenv()

# Initialize the agent (singleton)
agent = None

def get_agent():
    """Get or create the agent instance"""
    global agent
    if agent is None:
        agent = MovieAgent()
    return agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    # Startup
    logger.info("\n" + "="*60)
    logger.info("🚀 Starting IMDB Movie AI Agent API (FastAPI)")
    logger.info("="*60)
    logger.info("\n📍 Access URLs:")
    logger.info("   - Local:     http://localhost:8000/")
    logger.info("   - Network:   http://192.168.x.x:8000/")
    logger.info("   - Swagger:   http://localhost:8000/docs")
    logger.info("   - ReDoc:     http://localhost:8000/redoc")
    logger.info("\n📖 Examples:")
    logger.info("   - Search:    http://localhost:8000/api/movies/search?title=batman")
    logger.info("   - Health:    http://localhost:8000/api/health")
    logger.info("\n💡 Interactive API docs available at /docs")
    logger.info("="*60 + "\n")
    
    yield
    
    # Shutdown
    global agent
    if agent is not None:
        agent.close()
        agent = None
        logger.info("\n✅ Agent closed successfully.")

# Initialize FastAPI app
app = FastAPI(
    title="🎬 IMDB Movie AI Agent API",
    description="REST API to query movie database using AI Agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
async def home():
    """Home endpoint with API documentation"""
    return {
        'message': '🎬 IMDB Movie AI Agent API',
        'version': '1.0.0',
        'documentation': {
            'swagger_ui': '/docs',
            'redoc': '/redoc'
        },
        'endpoints': {
            'GET /api/movies/search': 'Search movies by title',
            'GET /api/movies/director': 'Get movies by director',
            'GET /api/movies/top': 'Get top rated movies',
            'GET /api/movies/genre': 'Get movies by genre',
            'GET /api/movies/year-range': 'Get movies by year range',
            'GET /api/movies/actor': 'Get movies with actor',
            'GET /api/movies/statistics': 'Get database statistics',
            'POST /api/query': 'Query the AI agent with natural language',
            'GET /api/health': 'Health check endpoint',
            'GET /api/cache/stats': 'Get cache statistics',
            'DELETE /api/cache/clear': 'Clear cache entries'
        }
    }

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return empty response for favicon requests"""
    return Response(status_code=204)

@app.get("/api/movies/search")
async def search_movies(title: str = Query(..., description="Movie title or partial title")):
    """
    Search movies by title (case-insensitive partial match)
    
    - **title**: Movie title or partial title to search for
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.search_movies_by_title(title)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/director")
async def movies_by_director(name: str = Query(..., description="Director's name")):
    """
    Get all movies by a specific director
    
    - **name**: Director's name or partial name
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_director(name)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/top")
async def top_movies(limit: int = Query(10, description="Number of movies to return", ge=1, le=50)):
    """
    Get top rated movies from the database
    
    - **limit**: Number of movies to return (1-50, default: 10)
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_top_rated_movies(limit)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/genre")
async def movies_by_genre(genre: str = Query(..., description="Movie genre")):
    """
    Get movies by genre
    
    - **genre**: Genre name (e.g., Action, Drama, Comedy)
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_genre(genre)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/year-range")
async def movies_by_year_range(
    start: int = Query(..., description="Start year", ge=1800, le=2100),
    end: int = Query(..., description="End year", ge=1800, le=2100)
):
    """
    Get movies within a year range
    
    - **start**: Start year (inclusive)
    - **end**: End year (inclusive)
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_year_range(start, end)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/actor")
async def movies_with_actor(name: str = Query(..., description="Actor's name")):
    """
    Get movies featuring a specific actor
    
    - **name**: Actor's name or partial name
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_with_actor(name)
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/movies/statistics")
async def movies_statistics():
    """
    Get statistical information about the movie database
    
    Returns total movies, average rating, year range, and top directors
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movie_statistics()
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def query_agent(query: QueryRequest):
    """
    Query the AI agent with natural language
    
    - **question**: Natural language question about movies
    
    Example: "What are the best movies from the 1990s?"
    """
    try:
        agent_instance = get_agent()
        response = agent_instance.query(query.question)
        return QueryResponse(question=query.question, answer=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Returns the status of the API, database connection, agent, and cache
    """
    try:
        agent_instance = get_agent()
        cache_stats = agent_instance.db_tools.cache.get_stats()
        return {
            'status': 'healthy',
            'database': 'connected',
            'agent': 'ready',
            'cache': cache_stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={'status': 'unhealthy', 'error': str(e)}
        )

@app.get("/api/cache/stats")
async def get_cache_stats():
    """
    Get Redis cache statistics
    
    Returns cache hit rate, memory usage, and key count
    """
    try:
        agent_instance = get_agent()
        stats = agent_instance.db_tools.cache.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/cache/clear")
async def clear_cache(pattern: str = Query("movie_cache:*", description="Key pattern to clear")):
    """
    Clear cache entries matching a pattern
    
    - **pattern**: Redis key pattern (default: movie_cache:*)
    """
    try:
        agent_instance = get_agent()
        count = agent_instance.db_tools.cache.clear_pattern(pattern)
        return {
            'message': f'Cache cleared successfully',
            'keys_deleted': count,
            'pattern': pattern
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))