"""
Flask API for IMDB Movie AI Agent
Provides REST endpoints to query the movie database
"""

from flask import Flask, request, jsonify
from agent import MovieAgent
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize the agent (singleton)
agent = None

def get_agent():
    """Get or create the agent instance"""
    global agent
    if agent is None:
        agent = MovieAgent()
    return agent

@app.route('/')
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': '🎬 IMDB Movie AI Agent API',
        'version': '1.0',
        'endpoints': {
            'GET /api/movies/search': 'Search movies by title',
            'GET /api/movies/director': 'Get movies by director',
            'GET /api/movies/top': 'Get top rated movies',
            'GET /api/movies/genre': 'Get movies by genre',
            'GET /api/movies/year-range': 'Get movies by year range',
            'GET /api/movies/actor': 'Get movies with actor',
            'GET /api/movies/statistics': 'Get database statistics',
            'POST /api/query': 'Query the AI agent with natural language'
        }
    })

@app.route('/api/movies/search', methods=['GET'])
def search_movies():
    """
    Search movies by title
    Query params: title (required)
    Example: /api/movies/search?title=batman
    """
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'Missing required parameter: title'}), 400
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.search_movies_by_title(title)
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/director', methods=['GET'])
def movies_by_director():
    """
    Get movies by director
    Query params: name (required)
    Example: /api/movies/director?name=nolan
    """
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing required parameter: name'}), 400
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_director(name)
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/top', methods=['GET'])
def top_movies():
    """
    Get top rated movies
    Query params: limit (optional, default 10)
    Example: /api/movies/top?limit=20
    """
    limit = request.args.get('limit', 10)
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_top_rated_movies(limit)
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/genre', methods=['GET'])
def movies_by_genre():
    """
    Get movies by genre
    Query params: genre (required)
    Example: /api/movies/genre?genre=action
    """
    genre = request.args.get('genre')
    if not genre:
        return jsonify({'error': 'Missing required parameter: genre'}), 400
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_genre(genre)
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/year-range', methods=['GET'])
def movies_by_year_range():
    """
    Get movies by year range
    Query params: start (required), end (required)
    Example: /api/movies/year-range?start=1990&end=2000
    """
    start = request.args.get('start')
    end = request.args.get('end')
    
    if not start or not end:
        return jsonify({'error': 'Missing required parameters: start and end'}), 400
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_by_year_range(int(start), int(end))
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except ValueError:
        return jsonify({'error': 'start and end must be valid years'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/actor', methods=['GET'])
def movies_with_actor():
    """
    Get movies with specific actor
    Query params: name (required)
    Example: /api/movies/actor?name=dicaprio
    """
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Missing required parameter: name'}), 400
    
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movies_with_actor(name)
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/movies/statistics', methods=['GET'])
def movies_statistics():
    """
    Get database statistics
    Example: /api/movies/statistics
    """
    try:
        agent_instance = get_agent()
        result = agent_instance.db_tools.get_movie_statistics()
        return jsonify(json.loads(result))
    except json.JSONDecodeError:
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/query', methods=['POST'])
def query_agent():
    """
    Query the AI agent with natural language
    Body: { "question": "What are the best movies from the 1990s?" }
    Example: POST /api/query
    """
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'error': 'Missing required field: question'}), 400
    
    question = data['question']
    
    try:
        agent_instance = get_agent()
        response = agent_instance.query(question)
        return jsonify({
            'question': question,
            'answer': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        agent_instance = get_agent()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'agent': 'ready'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# Cleanup on shutdown
@app.teardown_appcontext
def cleanup(error=None):
    """Close agent connection when app context tears down"""
    global agent
    if agent is not None:
        agent.close()
        agent = None

if __name__ == '__main__':
    print("🚀 Starting IMDB Movie AI Agent API...")
    print("📖 API documentation available at: http://localhost:5000/")
    print("🔍 Example: http://localhost:5000/api/movies/search?title=batman")
    print("💡 Use POST /api/query for natural language queries\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
