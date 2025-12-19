"""
LangChain AI Agent for IMDB Movie Database
Provides intelligent querying and analysis of movie data using MongoDB

This file:
- Connects to MongoDB (movie collection)
- Exposes "tools" (functions) to search for movies
- Sets up a LangChain ReAct (Reason + Act) agent that chooses the tools
"""

from langchain.agents import create_agent  # New LangChain 1.0+ API
from langchain_ollama import ChatOllama  # LLM (model) accessible via Ollama (local server)
from langchain_core.tools import Tool  # LangChain wrapper to declare functions usable by the agent
from pymongo import MongoClient  # Official MongoDB client for Python
from dotenv import load_dotenv  # Load environment variables from .env file
import os  # OS access (environment variables, etc.)
import json  # JSON serialization for clean output
from typing import List, Dict, Any  # Types for annotation (readability, IDE, type checking)

# Automatically load variables defined in ".env" file (in current directory)
load_dotenv()

# Disable (optional) LangSmith tracing by forcing the environment variable to "false"
# (useful if you don't want to send traces / or avoid a warning)
os.environ["LANGCHAIN_TRACING_V2"] = "false"

# Fix for Pydantic v2 compatibility with LangChain - must import cache first
try:
    from langchain_core.caches import BaseCache
    from langchain_core.globals import set_llm_cache
    # Initialize with no cache to avoid the error
    set_llm_cache(None)
except ImportError:
    pass

class MovieDatabaseTools:
    """Tools for querying the IMDB movie database

    This class encapsulates MongoDB access and provides search methods.
    The LangChain agent will call these methods via "Tool".
    """

    def __init__(self):
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('MONGODB_DATABASE')
        collection_name = os.getenv('MONGODB_COLLECTION')

        self.client = MongoClient(mongodb_uri)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def search_movies_by_title(self, title: str) -> str:
        """Search for movies by title (case-insensitive partial match)

        Param:
            title: title fragment (e.g. "batman")
        Return:
            JSON string of found movies (max 5) or error message
        """
        try:
            # Execute a MongoDB query:
            # - filter: title match via regex (partial) case-insensitive ($options: 'i')
            # - projection: exclude _id field (otherwise ObjectId not JSON-friendly)
            cursor = self.collection.find(
                {"title": {"$regex": title, "$options": "i"}},
                {"_id": 0},
            )
            movies = list(cursor)

            if not movies:
                return f"No movies found matching '{title}'"

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # In case of error (connection, query...), return message for debug
            return f"Error searching movies: {str(e)}"

    def get_movies_by_director(self, director: str) -> str:
        """Get all movies by a specific director

        Param:
            director: name (or fragment) of the director
        """
        try:
            # Query: director match case-insensitive regex
            # Projection: return only a few useful fields
            cursor = self.collection.find(
                {"director": {"$regex": director, "$options": "i"}},
                {"_id": 0, "title": 1, "year": 1, "imdb_rating": 1, "genre": 1},
            )
            movies = list(cursor)

            if not movies:
                return f"No movies found for director '{director}'"

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Capture and return the error
            return f"Error getting movies by director: {str(e)}"

    def get_top_rated_movies(self, limit: int = 10) -> str:
        """Get top rated movies from the database

        Param:
            limit: number of movies to return (capped at 50)
        """
        try:
            # Convert limit to int and apply a max cap of 50 to avoid huge returns
            limit = min(int(limit), 50)

            # Query without filter {} => all docs
            # Projection: useful fields
            cursor = self.collection.find(
                {},
                {"_id": 0, "title": 1, "year": 1, "imdb_rating": 1, "director": 1, "genre": 1},
            )
            movies = list(cursor.sort("imdb_rating", -1).limit(limit))

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Return the error as plain text
            return f"Error getting top rated movies: {str(e)}"

    def get_movies_by_genre(self, genre: str) -> str:
        """Get movies by genre (can be partial match)

        Param:
            genre: e.g. "Action" or "Drama"
        """
        try:
            # Query: genre match case-insensitive regex
            cursor = self.collection.find(
                {"genre": {"$regex": genre, "$options": "i"}},
                {"_id": 0, "title": 1, "year": 1, "imdb_rating": 1, "genre": 1, "director": 1},
            )
            movies = list(cursor)

            if not movies:
                return f"No movies found for genre '{genre}'"

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Error handling
            return f"Error getting movies by genre: {str(e)}"

    def get_movies_by_year_range(self, start_year: int, end_year: int) -> str:
        """Get movies released within a year range

        Params:
            start_year: start year (inclusive)
            end_year: end year (inclusive)
        """
        try:
            # MongoDB filter: year between start_year and end_year inclusive via $gte / $lte
            cursor = self.collection.find(
                {"year": {"$gte": int(start_year), "$lte": int(end_year)}},
                {"_id": 0, "title": 1, "year": 1, "imdb_rating": 1, "director": 1},
            )
            movies = list(cursor)

            if not movies:
                return f"No movies found between {start_year} and {end_year}"

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Error handling
            return f"Error getting movies by year range: {str(e)}"

    def get_movies_with_actor(self, actor: str) -> str:
        """Get movies featuring a specific actor

        Param:
            actor: name (or fragment) of the actor
        """
        try:
            # Query: stars match case-insensitive regex.
            # Note: if "stars" is a list, MongoDB applies the match on elements too.
            cursor = self.collection.find(
                {"stars": {"$regex": actor, "$options": "i"}},
                {"_id": 0, "title": 1, "year": 1, "imdb_rating": 1, "stars": 1, "director": 1},
            )
            movies = list(cursor)

            if not movies:
                return f"No movies found with actor '{actor}'"

            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Error handling
            return f"Error getting movies with actor: {str(e)}"

    def get_movie_statistics(self, query: str = "") -> str:
        """Get statistical information about movies in the database

        Param:
            query: (not used here) could be used to filter stats later.
        """
        try:
            # Count the total number of documents in the collection
            total_movies = self.collection.count_documents({})

            # MongoDB aggregation pipeline:
            # - group on a single group (_id None)
            # - calculate the average of imdb_rating field
            avg_rating = list(
                self.collection.aggregate(
                    [
                        {"$group": {"_id": None, "avg_rating": {"$avg": "$imdb_rating"}}}
                    ]
                )
            )[0]["avg_rating"]

            # Find min and max year via sorted find_one
            year_range = {
                "earliest": self.collection.find_one(sort=[("year", 1)])["year"],
                "latest": self.collection.find_one(sort=[("year", -1)])["year"],
            }

            top_directors = list(self.collection.aggregate([
                {'$group': {'_id': '$director', 'count': {'$sum': 1}, 'avg_rating': {'$avg': '$imdb_rating'}}},
                {'$sort': {'count': -1}},
                {'$limit': 10}
            ]))

            stats = {
                'total_movies': total_movies,
                'average_rating': round(avg_rating, 2),
                'year_range': year_range,
                'top_directors': top_directors
            }

            return json.dumps(stats, indent=2, default=str)
        except Exception as e:
            return f"Error getting statistics: {str(e)}"

    def advanced_search(self, query: str) -> str:
        """
        Advanced search using natural language query.
        Searches across title, overview, director, and genre.

        Here we assume a 'searchable_text' field exists (concatenation of info),
        which allows a simple regex match.
        """
        try:
            # Query: regex match on searchable_text
            cursor = self.collection.find(
                {"searchable_text": {"$regex": query, "$options": "i"}},
                {"_id": 0},
            )

            # Sort by rating and limit to 10
            movies = list(cursor.sort("imdb_rating", -1).limit(10))

            # If empty => message
            if not movies:
                return f"No movies found matching '{query}'"

            # Return JSON
            return json.dumps(movies, indent=2, default=str)
        except Exception as e:
            # Error handling
            return f"Error in advanced search: {str(e)}"


class MovieAgent:
    """AI Agent for interacting with the movie database

    This class:
    - instantiates MovieDatabaseTools
    - configures the LLM via Ollama
    - declares tools for LangChain
    - builds a ReAct agent + executor
    """

    @staticmethod
    def clean_input(text: str) -> str:
        """Remove extra quotes from input

        Purpose: some models return inputs surrounded by quotes.
        We remove them to make the tools more robust.
        """
        # Check that text is indeed a string
        if isinstance(text, str):
            # strip() removes spaces; strip("'\"") also removes single/double quotes from edges
            return text.strip().strip("'\"")

        # If it's not a str, return it as is
        return text

    def __init__(self):
        # Initialize DB access (MongoDB)
        self.db_tools = MovieDatabaseTools()

        # Get Ollama URL from environment (e.g. http://localhost:11434)
        ollama_base_url = os.getenv("OLLAMA_BASE_URL")

        # Get preferred model from environment
        preferred_model = os.getenv("OLLAMA_MODEL")

        # List of candidate models, in order:
        # - first the preferred one (may be None)
        # - then known fallbacks
        candidate_models = [
            preferred_model,
            "mistral",
            "llama3.2",
            "llama3.1",
            "qwen2.5",
        ]

        # List of initialization error messages, useful if no model works
        init_errors = []

        # Placeholder for the LLM (will be assigned once a model works)
        self.llm = None

        # Try models one by one until finding one that initializes
        for model_name in candidate_models:
            try:
                # Try to create a ChatOllama instance (server connection + model)
                self.llm = ChatOllama(
                    model=model_name,
                    base_url=ollama_base_url,
                    temperature=0,  # 0 => more deterministic outputs (less creativity)
                )

                # Console log to know which model was selected
                print(f"✅ Using Ollama model: {model_name} ({ollama_base_url})")

                # Exit the loop as soon as we have an LLM
                break
            except Exception as e:
                # If this model fails, store the error and move to the next
                init_errors.append(f"{model_name}: {e}")

        # If after the loop we still don't have an LLM, stop with a clear error
        if self.llm is None:
            raise RuntimeError(
                "Unable to initialize ChatOllama with available models. Make sure Ollama is started.\nErrors:\n- "
                + "\n- ".join(init_errors)
            )

        # Declare LangChain tools: each Tool has a name, a callable function, and a description.
        # We clean the input (clean_input) to avoid annoying quotes.
        self.tools = [
            Tool(
                name="search_movies_by_title",  # name used by the agent in "Action:"
                func=lambda x: self.db_tools.search_movies_by_title(self.clean_input(x)),  # cleaning wrapper
                description="Search for movies by title. Input should be a movie title or partial title.",
            ),
            Tool(
                name="get_movies_by_director",
                func=lambda x: self.db_tools.get_movies_by_director(self.clean_input(x)),
                description="Get all movies by a specific director. Input should be the director's name.",
            ),
            Tool(
                name="get_top_rated_movies",
                func=lambda x: self.db_tools.get_top_rated_movies(self.clean_input(x)),
                description="Get top rated movies. Input should be the number of movies to return (default 10).",
            ),
            Tool(
                name="get_movies_by_genre",
                func=lambda x: self.db_tools.get_movies_by_genre(self.clean_input(x)),
                description="Get movies by genre. Input should be a genre like Action, Drama, Comedy, etc.",
            ),
            Tool(
                name="get_movies_by_year_range",
                # Here the tool expects "start_year, end_year" separated by comma.
                # We split on ',' then clean and convert each part to int.
                func=lambda x: self.db_tools.get_movies_by_year_range(
                    *[int(y.strip().strip("'\"")) for y in self.clean_input(x).split(",")]
                ),
                description="Get movies within a year range. Input should be start_year, end_year (e.g., 1990, 2000).",
            ),
            Tool(
                name="get_movies_with_actor",
                func=lambda x: self.db_tools.get_movies_with_actor(self.clean_input(x)),
                description="Get movies featuring a specific actor. Input should be the actor's name.",
            ),
            Tool(
                name="get_movie_statistics",
                # Here the input is not used: we return global stats.
                func=lambda x: self.db_tools.get_movie_statistics(),
                description="Get statistical information about the movie database. No input required, just use 'stats' as input.",
            ),
            Tool(
                name="advanced_search",
                func=lambda x: self.db_tools.advanced_search(self.clean_input(x)),
                description="Advanced search across all movie fields. Use for complex queries about plot, themes, or combinations of criteria.",
            ),
        ]

        # System prompt for the agent (replaces the old template)
        system_prompt = """You are a helpful assistant that answers questions about movies in the IMDB database.

You have access to tools to search and analyze movie data. Use the tools to find information, then provide a clear and helpful answer.

When using tools:
- Use search_movies_by_title to find movies by name
- Use get_movies_by_director to find movies by a specific director
- Use get_top_rated_movies to find the highest rated movies
- Use get_movies_by_genre to find movies of a specific genre
- Use get_movies_by_year_range to find movies from a time period
- Use get_movies_with_actor to find movies featuring an actor
- Use get_movie_statistics to get overall database statistics
- Use advanced_search for complex queries across all fields

Always provide complete, helpful answers based on the data you find."""

        # Create the agent using the new LangChain 1.0+ API
        # This is much simpler than the old ReAct agent + AgentExecutor approach
        self.agent = create_agent(
            model=self.llm,  # the LLM model
            tools=self.tools,  # the declared tools
            system_prompt=system_prompt,  # instructions for the agent
        )

    def query(self, question: str) -> str:
        """Query the agent with a question

        Param:
            question: natural language question (e.g. "top 5 movies")
        Return:
            final output from the agent (string)
        """
        try:
            # In LangChain 1.0+, the agent is invoked with messages
            result = self.agent.invoke({"messages": [{"role": "user", "content": question}]})
            
            # Extract the final message from the agent's response
            messages = result.get("messages", [])
            if messages:
                # Get the last message (the agent's final response)
                last_message = messages[-1]
                # Handle both dict and object formats
                if isinstance(last_message, dict):
                    return last_message.get("content", str(last_message))
                else:
                    return getattr(last_message, "content", str(last_message))
            
            return "No response generated"
        except Exception as e:
            # In case of error, return a debug message
            return f"Error processing query: {str(e)}"

    def close(self):
        """Close database connection

        Important: releases resources (MongoDB connection).
        """
        # Properly close the MongoDB connection
        self.db_tools.client.close()


# Entry point if this file is executed directly (python movie_agent.py)
if __name__ == "__main__":
    # Instantiate the agent (DB connection + LLM init + tools + agent)
    agent = MovieAgent()

    # Simple message to confirm init
    print("Movie AI Agent initialized!")

    # Display example questions the user can ask
    print("\nExample queries:")
    print("1. What are the top 5 rated movies?")
    print("2. Show me Christopher Nolan movies")
    print("3. Find action movies from the 2000s")
    print("4. What movies has Leonardo DiCaprio been in?")

    # Close the DB connection (good practice)
    agent.close()