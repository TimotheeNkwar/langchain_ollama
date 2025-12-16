"""
LangChain AI Agent for IMDB Movie Database
Provides intelligent querying and analysis of movie data using MongoDB

This file:
- Connects to MongoDB (movie collection)
- Exposes "tools" (functions) to search for movies
- Sets up a LangChain ReAct (Reason + Act) agent that chooses the tools
"""

# Import: AgentExecutor executes the agent + tools, create_react_agent builds a ReAct agent
try:
    from langchain.agents import AgentExecutor, create_react_agent
except ImportError:
    from langchain_core.agents import AgentExecutor
    from langchain.agents import create_react_agent

# Import: ChatOllama is the LLM (model) accessible via Ollama (local server)
from langchain_ollama import ChatOllama

# Import: Tool is a LangChain wrapper to declare functions usable by the agent
from langchain_core.tools import Tool

# Import: hub allows using LangChain Hub (hosted prompts/tools), used here via hub.run(...)
from langchain import hub

# Import : client officiel MongoDB pour Python
from pymongo import MongoClient

# Import : charge les variables d'environnement depuis un fichier .env (si présent)
from dotenv import load_dotenv

# Import : accès OS (variables d'env, etc.)
import os

# Import : sérialisation JSON pour afficher proprement les résultats
import json

# Import : types pour l'annotation (lisibilité, IDE, vérifications)
from typing import List, Dict, Any

# Charge automatiquement les variables définies dans un fichier ".env" (dans le dossier courant)
load_dotenv()

# Désactive (optionnel) le tracing LangSmith en forçant la variable d'environnement à "false"
# (utile si tu ne veux pas envoyer de traces / ou éviter un warning)
os.environ["LANGCHAIN_TRACING_V2"] = "false"

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
        # Vérifie que text est bien une chaîne
        if isinstance(text, str):
            # strip() enlève espaces; strip("'\"") enlève aussi guillemets simples/doubles en bord
            return text.strip().strip("'\"")

        # Si ce n'est pas une str, on le renvoie tel quel
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
            Tool(
                name="hub_search_movies",
                # Call LangChain Hub passing it a text query.
                # Note: hub.run depends on what LangChain Hub provides; this is not MongoDB.
                func=lambda x: hub.run(f"search movies titled '{self.clean_input(x)}'"),
                description="Use LangChain Hub to search for movies by title with enhanced capabilities. Input should be a movie title or partial title.",
            ),
        ]

        # Local import (in __init__): avoids loading PromptTemplate if we don't instantiate the agent.
        from langchain.prompts import PromptTemplate

        # ReAct prompt template:
        # - describes available tools
        # - imposes strict "Question/Thought/Action/Action Input/Observation" format
        template = """You are a helpful assistant that answers questions about movies in the IMDB database.

You have access to the following tools:

{tools}

IMPORTANT: Use this EXACT format (each on a separate line):

Question: the input question
Thought: think about what to do
Action: one of [{tool_names}]
Action Input: the input for the action (without quotes or parentheses)
Observation: the result will appear here
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the complete answer to the question

EXAMPLE:
Question: What are the top 5 movies?
Thought: I should get the top rated movies from the database
Action: get_top_rated_movies
Action Input: 5
Observation: [results will be shown here]
Thought: I now have the information needed
Final Answer: Here are the top 5 movies...

BEGIN!

Question: {input}
Thought:{agent_scratchpad}"""

        # Build a LangChain PromptTemplate from the string
        self.prompt = PromptTemplate.from_template(template)

        # Build the ReAct agent:
        # - self.llm: the model
        # - self.tools: list of tools
        # - self.prompt: instructions + format
        self.agent = create_react_agent(self.llm, self.tools, self.prompt)

        # AgentExecutor: orchestrator that:
        # - launches the agent
        # - executes the tools
        # - manages the Thought/Action/Observation loop
        self.agent_executor = AgentExecutor(
            agent=self.agent,  # the ReAct agent
            tools=self.tools,  # the declared tools
            verbose=True,  # displays steps (debug)
            max_iterations=5,  # limits the loop to avoid infinite loops
            handle_parsing_errors=True,  # tries to survive poorly formatted model outputs
        )

    def query(self, question: str) -> str:
        """Query the agent with a question

        Param:
            question: natural language question (e.g. "top 5 movies")
        Return:
            final output from the agent (string)
        """
        try:
            # invoke expects a dict of inputs according to the prompt: here {input: question}
            response = self.agent_executor.invoke({"input": question})

            # The AgentExecutor often returns a dict containing "output"
            return response["output"]
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
