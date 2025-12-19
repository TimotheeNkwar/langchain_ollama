# 🎬 TMDB Movie AI Agent with MongoDB and LangChain

An intelligent AI agent with **REST API** built with **LangChain 1.0+**, **FastAPI**, and **MongoDB** that can answer questions about 50,000 movies from The Movie Database (TMDB). The agent uses Ollama (local LLM) to understand natural language queries and intelligently retrieves information from a MongoDB database.

## 🌟 Features

- **Natural Language Queries**: Ask questions in plain English
- **REST API with FastAPI**: 10 endpoints with automatic OpenAPI documentation
- **Modern Web Frontend**: React + Vite with Netflix-inspired UI
- **Interactive CLI**: Command-line interface for direct interaction
- **Intelligent Search**: Search movies by title, director, actor, genre, year, and more
- **AI Chat Interface**: Real-time chat with AI assistant in the browser
- **Smart Recommendations**: Get movie recommendations based on preferences
- **Advanced Filters**: Multi-criteria search (genre, year, rating, director, actor)
- **Statistical Analysis**: Get insights about the movie database
- **MongoDB Integration**: Efficient data storage and retrieval
- **LangChain 1.0+ Agent**: Modern create_agent API with automatic tool selection
- **Responsive Design**: Mobile-friendly interface
- **Centralized Logging**: Loguru with rotation, retention, and separate log files (agent.log, api.log, main.log)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                      │
│   CLI (main.py) | REST API (api.py) | React Frontend   │
│                 Port 8000           | Port 3000         │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   LangChain 1.0+     │
              │   Agent (8 tools)    │
              └──────────┬───────────┘
                         │
              ┌──────────▼───────────┐
              │  Ollama (Local LLM)  │
              │ mistral/llama3.2/... │
              └──────────┬───────────┘
                         │
              ┌──────────▼───────────┐
              │   MongoDB Database   │
              │   50,000 movies      │
              └──────────────────────┘
```

The agent uses LangChain's 1.0+ create_agent API to:
1. Understand user intent via Ollama LLM
2. Automatically select appropriate database tools
3. Query MongoDB efficiently
4. Format responses in a user-friendly way

## 📋 Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- Ollama installed and running locally

## 🚀 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd c:\Users\timot\Desktop\langchain
```

### 2. Install MongoDB

**Option A: Local MongoDB (Windows)**
- Download from [MongoDB Community Server](https://www.mongodb.com/try/download/community)
- Install and start the MongoDB service
- Default connection: `mongodb://localhost:27017/`

**Option B: MongoDB Atlas (Cloud)**
- Sign up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Create a free cluster
- Get your connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/`)

### 3. Install Ollama

**Download and Install Ollama:**
- Visit [Ollama.ai](https://ollama.ai/)
- Download and install Ollama for Windows
- Start Ollama (it runs as a background service)

**Pull a Model:**
```bash
# Pull one of the supported models
ollama pull mistral
# or
ollama pull llama3.2
# or
ollama pull qwen2.5
```

Verify Ollama is running:
```bash
ollama list
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**
- langchain>=0.3.0 (Agent framework)
- fastapi>=0.109.0 (REST API)
- pymongo==4.6.1 (MongoDB driver)
- loguru>=0.7.2 (Advanced logging with rotation)

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` and add your configuration:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral  # or llama3.2, llama3.1, qwen2.5

# MongoDB Connection (choose one)
# For local MongoDB:
MONGODB_URI=mongodb://localhost:27017/

# For MongoDB Atlas:
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Database configuration
MONGODB_DATABASE=langchain_db
MONGODB_COLLECTION=movies
```

### 6. Load Data into MongoDB

Run the data ingestion script:

```bash
python data_ingestion.py
```

This will:
- Connect to MongoDB
- Load the IMDB CSV data
- Clean and structure the data
- Create indexes for optimal performance
- Display database statistics

Expected output:
```
Connecting to MongoDB...
Clearing existing data...
Reading CSV file...
Loaded 50000 movies from CSV
Inserting 50000 movies into MongoDB in batches...
Progress: 1000/50000 movies inserted (2.0%)
...
Progress: 50000/50000 movies inserted (100.0%)
Successfully inserted 50000 movies
Creating indexes...
Data ingestion complete!

=== Database Statistics ===
Total movies: 50000
Average TMDB rating: 6.2
Year range: 1874 - 2025
```

## 🎮 Usage

### Option 1: Interactive CLI Agent

```bash
python main.py
```

### Option 2: REST API Server

**Start the API:**
```bash
# Using Uvicorn directly
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# OR using the launcher script
python run_api.py
```

**Access the API:**
- API Base: `http://localhost:8000`
- Interactive Docs (Swagger): `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

### Option 3: React Web Frontend

**Start the frontend:**
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

**Access the frontend:**
- Web App: `http://localhost:3000`
- Features: Movie search, AI chat, advanced filters, Netflix-style UI

**Note:** The API server must be running on port 8000 for the frontend to work.

**Full Stack Setup:**
```bash
# Terminal 1: Start backend API
uvicorn api:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev
```

For complete frontend documentation, see [frontend/README.md](frontend/README.md).

**API Examples:**
```bash
# Search movies
curl "http://localhost:8000/api/movies/search?title=batman"

# Get top rated movies
curl "http://localhost:8000/api/movies/top?limit=5"

# Natural language query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the best sci-fi movies?"}'
```

For complete API documentation, see [API_README.md](API_README.md).

### Example Queries

**Search & Discovery:**
```
🎬 You: What are the top 10 rated movies?
🎬 You: Find movies about space or sci-fi
🎬 You: Show me Christopher Nolan movies
🎬 You: Search for Marvel movies
```

**Actor & Director Queries:**
```
🎬 You: What movies has Leonardo DiCaprio been in?
🎬 You: Show me all Quentin Tarantino films
🎬 You: Find movies with Tom Hanks
```

**Time-based Queries:**
```
🎬 You: What are the best movies from the 1990s?
🎬 You: Show me movies between 2000 and 2010
```

**Statistics & Analysis:**
```
🎬 You: What are the database statistics?
🎬 You: Who are the most prolific directors?
```

**Recommendations:**
```
🎬 You: Recommend a thriller movie
🎬 You: I want to watch something like Inception
🎬 You: Suggest a classic movie
```

## � Logging

The application uses **loguru** for centralized logging with automatic rotation and retention:

- **agent.log** - Agent operations, tool selection, query processing
- **api.log** - API requests, responses, server events
- **main.log** - CLI interactions, user queries, errors

**Configuration:**
- Rotation: 10 MB per file
- Retention: 7 days
- Format: `{time} | {level} | {name}:{function}:{line} - {message}`
- Backtrace: Enabled for debugging
- Console output: INFO level and above

Logs are automatically excluded from Git (.gitignore).

## �🛠️ Project Structure

```
langchain_ollama/
├── dataset/
│   ├── movies.csv             # Original IMDB dataset (deprecated)
│   ├── TMDB_movie_dataset_v50k.csv  # TMDB dataset (50,000 movies)
│  
│   └── data.ipynb            # Notebook to create subsets
├── frontend/                  # React Web Frontend
│   ├── src/
│   │   ├── components/       # React components (MovieCard, MovieSearch, AIChat)
│   │   ├── services/         # API service layer
│   │   ├── App.jsx           # Main app component
│   │   └── main.jsx          # Entry point
│   ├── package.json          # Dependencies (React, Vite, Axios)
│   ├── vite.config.js        # Vite configuration
│   └── README.md             # Frontend documentation
├── Project_summary/
│   ├── PROJECT_STRUCTURE.txt  # Detailed project structure documentation
│   └── PROJECT_SUMMARY.md     # Project overview and summary
├── testing/
│   └── test_setup.py          # Environment verification script
|      |_ test_api.py                # API testing script
├── agent.py                   # LangChain 1.0+ agent implementation
├── api.py                     # FastAPI REST API server (port 8000)
├── run_api.py                 # API launcher script
├── data_ingestion.py          # Script to load data into MongoDB
├── main.py                    # Interactive CLI application
├── requirements.txt           # Python dependencies
├── agent.log                  # Agent logs (auto-rotated, gitignored)
├── api.log                    # API logs (auto-rotated, gitignored)
├── main.log                   # Main logs (auto-rotated, gitignored)
├── .env.example               # Environment variables template
├── .env                       # Your configuration (create this)
├── .gitignore                 # Git ignore rules
├── LICENSE                    # Project license
├── README.md                  # This file (main documentation)
├── API_README.md              # FastAPI documentation
├── ARCHITECTURE.md            # System architecture documentation
└── QUICKSTART.md              # Quick setup guide
```

## 🔧 How It Works

### 1. Data Ingestion (`data_ingestion.py`)

- Reads the TMDB CSV file (limited to 50,000 movies)
- Cleans and transforms data with proper type conversion
- Stores structured documents in MongoDB using batch insertion
- Creates indexes for efficient querying on key fields

### 2. Movie Agent (`agent.py`)

**Tools Available (8 tools):**
- `search_movies_by_title`: Search by movie title
- `get_movies_by_director`: Find movies by director
- `get_top_rated_movies`: Get highest-rated movies
- `get_movies_by_genre`: Filter by genre
- `get_movies_by_year_range`: Filter by release year
- `get_movies_with_actor`: Find movies with specific actors
- `get_movie_statistics`: Database analytics
- `advanced_search`: Complex multi-field search

**Agent Workflow (LangChain 1.0+):**
1. Receives natural language query
2. Uses Ollama LLM (mistral/llama3.2/llama3.1/qwen2.5) to understand intent
3. Selects appropriate tool(s) automatically
4. Executes MongoDB queries
5. Formats and returns results

### 3. Main Application (`main.py`)

- Provides interactive CLI interface
- Handles user input/output
- Manages agent lifecycle
- Error handling and user guidance

### 4. FastAPI REST API (`api.py`)

- RESTful API endpoints for movie queries
- Automatic OpenAPI documentation at `/docs`
- CORS support for web applications
- 10 endpoints including health checks
- Runs on port 8000
- Start with: `uvicorn api:app --reload` or `python run_api.py`

## 📊 Database Schema

Each movie document in MongoDB contains:

```json
{
  "tmdb_id": 278,
  "imdb_id": "tt0111161",
  "title": "The Shawshank Redemption",
  "original_title": "The Shawshank Redemption",
  "year": 1994,
  "release_date": "1994-09-23",
  "runtime_minutes": 142,
  "genres": "Drama, Crime",
  "vote_average": 8.7,
  "vote_count": 26000,
  "overview": "Two imprisoned men bond over...",
  "tagline": "Fear can hold you prisoner. Hope can set you free.",
  "poster_path": "/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
  "backdrop_path": "/iNh3BivHyg5sQRPP1KOkzguEX0H.jpg",
  "popularity": 98.5,
  "budget": 25000000,
  "revenue": 28341469,
  "status": "Released",
  "original_language": "en",
  "production_companies": "Castle Rock Entertainment, Columbia Pictures",
  "production_countries": "United States of America",
  "spoken_languages": "English",
  "keywords": "prison, friendship, hope, redemption",
  "homepage": "https://...",
  "adult": false,
  "searchable_text": "Combined text for search"
}
```

## 🔍 Advanced Features

### Custom Queries

You can extend the agent by adding new tools in `agent.py`:

```python
Tool(
    name="your_custom_tool",
    func=self.db_tools.your_custom_function,
    description="Description for the AI to understand when to use this tool"
)
```

### MongoDB Aggregation

The agent uses MongoDB's aggregation pipeline for complex queries:

```python
self.collection.aggregate([
    {'$group': {'_id': '$director', 'count': {'$sum': 1}}},
    {'$sort': {'count': -1}},
    {'$limit': 10}
])
```

## 🐛 Troubleshooting

### MongoDB Connection Error

**Problem:** `pymongo.errors.ServerSelectionTimeoutError`

**Solutions:**
- Ensure MongoDB is running: `net start MongoDB` (Windows)
- Check connection string in `.env`
- For Atlas: Whitelist your IP address

### Ollama Connection Error

**Problem:** `Unable to initialize ChatOllama with available models`

**Solutions:**
- Ensure Ollama is installed and running
- Check if Ollama service is active: `ollama list`
- Verify the model is pulled: `ollama pull mistral`
- Check OLLAMA_BASE_URL in `.env` (default: `http://localhost:11434`)
- Try restarting Ollama

### No Movies Found

**Problem:** Agent returns "No movies found"

**Solutions:**
- Run `python data_ingestion.py` to load data
- Check MongoDB connection
- Verify database and collection names in `.env`

### Import Errors

**Problem:** `ModuleNotFoundError`

**Solutions:**
```bash
pip install -r requirements.txt --upgrade
```

## 📈 Performance Tips

1. **Indexes**: The ingestion script creates indexes automatically
2. **Limit Results**: Tools limit results to prevent overwhelming responses
3. **Connection Pooling**: MongoDB client handles connection pooling
4. **Caching**: Consider implementing caching for frequent queries

## 🔐 Security Best Practices

- Never commit `.env` file to version control
- Use environment variables for all configuration
- For production, use MongoDB Atlas with authentication
- Ollama runs locally - no API keys needed
- Use read-only database users when possible
- Keep Ollama updated to the latest version

## 🚀 Next Steps

**Enhancements you can add:**

1. **Vector Search**: Add embeddings for semantic search
2. **Web Frontend**: Build React/Vue.js frontend consuming the API
3. **Authentication**: Add JWT or OAuth2 to the API
4. **Rate Limiting**: Implement API rate limiting
5. **Caching**: Add Redis for frequent query caching
6. **More Data**: Expand with reviews, ratings, streaming availability
7. **Visualization**: Add charts and graphs for statistics
8. **Recommendations**: Implement collaborative filtering
9. **Multi-language**: Add support for multiple languages
10. **WebSockets**: Real-time streaming responses

## 📚 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Python Driver](https://pymongo.readthedocs.io/)
- [Ollama Documentation](https://ollama.ai/)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [TMDB Dataset](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies)
- [API Documentation](API_README.md) - Complete REST API reference

## 📝 License

This project is for educational purposes. The TMDB dataset is used under fair use for learning and demonstration.

## 🤝 Contributing

Feel free to fork, modify, and enhance this project! Some ideas:
- Add more sophisticated NLP features
- Implement user preferences and history
- Add movie recommendation algorithms
- Create a web dashboard

## 💡 Tips for Best Results

1. **Be Specific**: "Show me sci-fi movies from the 2000s" works better than "show movies"
2. **Use Natural Language**: The agent understands conversational queries
3. **Combine Criteria**: "Find highly-rated action movies with Tom Cruise"
4. **Ask for Statistics**: "What's the average rating of Nolan's movies?"

---

## 📖 Documentation

- **[README.md](README.md)** - This file (main documentation)
- **[API_README.md](API_README.md)** - Complete REST API documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture details
- **[PROJECT_SUMMARY.md](Project_summary/PROJECT_SUMMARY.md)** - Project overview

---

**Built with ❤️ using LangChain 1.0+, FastAPI, MongoDB, and Ollama**

Happy movie hunting! 🎬🍿
