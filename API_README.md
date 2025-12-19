# 🎬 TMDB Movie AI Agent - REST API Documentation

Modern REST API built with **FastAPI** for querying 50,000 movies using an intelligent AI agent powered by LangChain and Ollama.

## ✨ Features

- **10 RESTful Endpoints** - Comprehensive movie query capabilities
- **Automatic OpenAPI Documentation** - Interactive docs at `/docs` and `/redoc`
- **Natural Language Queries** - Ask questions in plain English via POST `/api/query`
- **CORS Enabled** - Ready for web applications and frontend frameworks
- **High Performance** - Built with FastAPI and async support
- **AI-Powered** - Uses LangChain 1.0+ and local Ollama LLMs

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Ensure your `.env` file contains:
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=langchain_db
MONGODB_COLLECTION=movies
```

### 3. Start the Server

**Option A: Using Uvicorn directly**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Option B: Using the launcher script**
```bash
python run_api.py
```

The API will be available at:
- **API Base**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 📖 API Endpoints

All endpoints are automatically documented with interactive examples at `/docs`.

### 1. **GET /** - API Welcome & Info
Returns API information and available endpoints.

**Example:**
```bash
curl http://localhost:8000/
```

**Response:**
```json
{
  "message": "🎬 IMDB Movie AI Agent API",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

---

### 2. **GET /api/health** - Health Check
Verifies that the API, database, and AI agent are operational.

**Example:**
```bash
curl http://localhost:8000/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "agent": "ready",
  "ollama_model": "mistral"
}
```

---

### 3. **GET /api/movies/search** - Search by Title
Search movies by title (partial match, case-insensitive).

**Query Parameters:**
- `title` (required): Movie title or partial title

**Example:**
```bash
curl "http://localhost:8000/api/movies/search?title=batman"
```

**Response:**
```json
{
  "movies": [
    {
      "title": "The Dark Knight",
      "year": 2008,
      "vote_average": 8.5,
      "director": "Christopher Nolan",
      "genres": ["Action", "Crime", "Drama"]
    }
  ],
  "count": 1
}
```

---

### 4. **GET /api/movies/top** - Top Rated Movies
Returns the highest-rated movies from the database.

**Query Parameters:**
- `limit` (optional, default: 10, max: 50): Number of movies to return

**Example:**
```bash
curl "http://localhost:8000/api/movies/top?limit=5"
```

**Response:**
```json
{
  "movies": [...],
  "count": 5,
  "limit": 5
}
```

---

### 5. **GET /api/movies/director** - Movies by Director
Find all movies by a specific director.

**Query Parameters:**
- `name` (required): Director's name or partial name

**Example:**
```bash
curl "http://localhost:8000/api/movies/director?name=nolan"
```

**Response:**
```json
{
  "director": "nolan",
  "movies": [
    {
      "title": "Inception",
      "year": 2010,
      "vote_average": 8.8
    }
  ],
  "count": 11
}
```

---

### 6. **GET /api/movies/genre** - Movies by Genre
Filter movies by genre.

**Query Parameters:**
- `genre` (required): Genre name (Action, Drama, Comedy, Sci-Fi, etc.)

**Example:**
```bash
curl "http://localhost:8000/api/movies/genre?genre=sci-fi"
```

**Response:**
```json
{
  "genre": "sci-fi",
  "movies": [...],
  "count": 1523
}
```

---

### 7. **GET /api/movies/year-range** - Movies by Year Range
Find movies released within a specific time period.

**Query Parameters:**
- `start` (required): Start year (inclusive)
- `end` (required): End year (inclusive)

**Example:**
```bashing

A comprehensive test script is provided to test all endpoints:

```bash
# Terminal 1: Start the API server
uvicorn api:app --reload

# Terminal 2: Run the tests
python test_api.py
```

**Manual Testing with curl:**
```bash
# Health check
curl http://localhost:8000/api/health

# Search for movies
curl "http://localhost:8000/api/movies/search?title=inception"

# Natural language query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me top rated sci-fi movies"}'
```

---

## 🌐 Frontend Integration Examples

### JavaScript Fetch API

```javascript
// Search movies by title
async function searchMovies(title) {
  const response = await fetch(
    `http://localhost:8000/api/movies/search?title=${encodeURIComponent(title)}`
  );
  const data = await response.json();
  return data.movies;
}

// Natural language query
async function queryAgent(question) {
  const response = await fetch('http://localhost:8000/api/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query: question })
  });
  const data = await response.json();
  return data.answer;
}

// Usage
const movies = await searchMovies('batman');
const answer = await queryAgent('What are the best Christopher Nolan movies?');
```

### Axios

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create an axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Search movies
const searchMovies = async (title) => {
  const { data } = await api.get('/api/movies/search', {
    params: { title }
  });
  return data.movies;
};

// Get top rated movies
const getTopMovies = async (limit = 10) => {
  const { data } = await api.get('/api/movies/top', {
    params: { limit }
  });
  return data.movies;
};

// Natural language query
const queryAgent = async (query) => {
  const { data } = await api.post('/api/query', { query });
  return data.answer;
};

// Usage
const movies = await searchMovies('inception');
const topMovies = await getTopMovies(5);
const answer = await queryAgent('Recommend a thriller movie');
```

### React Hook Example

```jsx
import { useState, useEffect } from 'react';

function MovieSearch() {
  const [query, setQuery] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);

  const searchMovies = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/movies/search?title=${query}`
      );
      const data = await response.json();
      setMovies(data.movies);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search movies..."
      />
      <button onClick={searchMovies} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
      <ul>
        {movies.map((movie, idx) => (
          <li key={idx}>
            {movie.title} ({movie.year}) - ⭐ {movie.vote_average}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### Vue.js Example

```vue
<template>
  <div>
    <input v-model="query" placeholder="Ask about movies..." />
    <button @click="askAgent" :disabled="loading">Ask AI</button>
    <div v-if="answer">{{ answer }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const query = ref('');
const answer = ref('');
const loading = ref(false);

const askAgent = async () => {
  loading.value = true;
  try {
    const response = await fetch('http://localhost:8000/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value })
    });
    const data = await response.json();
    answer.value = data.answer;
  } finally {
    loading.value = false;
  }
};
</script>
curl http://localhost:8000/api/movies/statistics
```

**Response:**
```json
{
  "total_movies": 50000,
  "average_rating": 6.2,
  "year_range": {
    "earliest": 1874,
    "latest": 2025
  },
  "top_directors": [
    {
      "_id": "Steven Spielberg",
      "count": 34,
      "avg_rating": 7.5
    }
  ]
}
```

---

### 10. **POST /api/query** - Natural Language Query
Query the AI agent with natural language questions. The agent will automatically select and use the appropriate tools.

**Request Body (JSON):**
```json
{
  "query": "What are the best sci-fi movies from the 2000s?"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the top 3 Christopher Nolan movies?"}'
```

**Response:**
```json
{
  "query": "What are the top 3 Christopher Nolan movies?",
  "answer": "Based on the TMDB database, here are the top 3 Christopher Nolan movies by rating:\n\n1. The Dark Knight (2008) - 8.5/10\n2. Inception (2010) - 8.8/10\n3. Interstellar (2014) - 8.6/10\n\nAll three are critically acclaimed masterpieces that showcase Nolan's unique storytelling style.",
  "processing_time": 3.42
}
```

## 🧪 Tests

Un script de test est fourni pour tester tous les endpoints :

```bash
# Démarrer l'API dans un terminal
python api.py

# Dans un autre terminal, exécuter les tests
python test_api.py
```

## 🌐 Utilisation avec JavaScript/Frontend

### Exemple avec Fetch API :

```javascript
// Recherche de films
fetch('http://localhost:5000/api/movies/search?title=batman')
  .then(response => response.json())
  .then(data => console.log(data));

// Requête en langage naturel
fetch('http://localhost:5000/api/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What are the best sci-fi movies?'
  })
})
  .then(response => response.json())
  .then(data => console.log(data.answer));
```

### Exemple avec Axios :

```javascript
import axios from 'axios';

// Recherche de films
const movies = await axios.get('http://localhost:5000/api/movies/search', {
  params: { title: 'batman' }
});

// Requête en langage naturel
const response = await axios.post('http://localhost:5000/api/query', {
  question: 'What are the best sci-fi movies?'
});
console.log(response.data.answer);
```

---

## 🔧 Configuration

### Environment Variables

All configuration is managed through environment variables in `.env`:

```env
# Ollama LLM Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral  # or llama3.2, llama3.1, qwen2.5

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=langchain_db
MONGODB_COLLECTION=movies

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000
```

### CORS Configuration

CORS is enabled by default for all origins. To restrict access, modify `api.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Development vs Production

**Development (with auto-reload):**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Production (with multiple workers):**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## 📝 Error Handling

The API returns standard HTTP status codes with detailed error messages:

| Status Code | Description |
|-------------|-------------|
| **200** | Success |
| **400** | Bad Request - Missing or invalid parameters |
| **404** | Not Found - Endpoint doesn't exist |
| **422** | Validation Error - Invalid request body |
| **500** | Internal Server Error |
| **503** | Service Unavailable - Database or agent connection issue |

**Error Response Format:**
```json
{
  "detail": "Missing required parameter: title"
}
```

**Example Error Handling:**
```javascript
try {
  const response = await fetch('http://localhost:8000/api/movies/search?title=batman');
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
  }
  const data = await response.json();
  console.log(data);
} catch (error) {
  console.error('Network Error:', error);
}
```

---

## 🚀 Deployment

### Production Deployment with Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Build and Run:**
```bash
docker build -t movie-api .
docker run -p 8000:8000 --env-file .env movie-api
```

### Deployment with Gunicorn + Uvicorn Workers

For production with better performance:

```bash
pip install gunicorn

gunicorn api:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

### Reverse Proxy with Nginx

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTPS with Let's Encrypt

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

### Cloud Deployment Options

- **AWS**: Deploy on EC2, ECS, or Lambda with API Gateway
- **Google Cloud**: Cloud Run or GKE
- **Azure**: App Service or Container Instances
- **Heroku**: Simple deployment with Procfile
- **Railway**: One-click deployment
- **Render**: Easy FastAPI deployment

---

## 💡 Best Practices & Tips

### Performance Optimization
- ✅ **Agent Singleton**: Agent is initialized once at startup for optimal performance
- ✅ **Connection Pooling**: MongoDB connections are automatically pooled
- ✅ **Async Operations**: FastAPI runs asynchronously by default
- ✅ **Response Caching**: Consider adding Redis for frequently requested data
- ✅ **Query Limits**: All list endpoints are limited to prevent overload

### Security Recommendations
- 🔒 **Environment Variables**: Never commit `.env` files
- 🔒 **API Keys**: Add authentication for production (JWT, OAuth2)
- 🔒 **Rate Limiting**: Implement rate limiting to prevent abuse
- 🔒 **HTTPS Only**: Use SSL/TLS in production
- 🔒 **Input Validation**: FastAPI provides automatic validation via Pydantic

### Monitoring & Logging
- 📊 **Add Logging**: Use structured logging (e.g., loguru)
- 📊 **Metrics**: Track API usage, response times, error rates
- 📊 **Health Checks**: Use `/api/health` for monitoring
- 📊 **APM Tools**: Consider Datadog, New Relic, or Sentry

### Scaling Strategies
- 📈 **Horizontal Scaling**: Run multiple Uvicorn workers
- 📈 **Load Balancing**: Use Nginx or cloud load balancers
- 📈 **Caching**: Redis for frequent queries and responses
- 📈 **Database Indexing**: Ensure MongoDB has proper indexes
- 📈 **CDN**: Serve static assets via CDN if needed

---

## 🎯 Use Cases

### 1. Movie Search Web Application
Build a React/Vue/Angular frontend that consumes this API for movie searches and recommendations.

### 2. Mobile App Backend
Use as the backend for iOS/Android movie discovery apps.

### 3. Chatbot Integration
Integrate with Slack, Discord, or Telegram bots for movie recommendations.

### 4. Data Analysis
Use the statistics endpoint for movie trend analysis and visualization.

### 5. Content Management System
Integrate with WordPress or other CMS for movie content.

---

## 📚 Additional Resources

- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **LangChain Documentation**: [https://python.langchain.com/](https://python.langchain.com/)
- **Ollama Documentation**: [https://ollama.ai/](https://ollama.ai/)
- **MongoDB Documentation**: [https://docs.mongodb.com/](https://docs.mongodb.com/)
- **Uvicorn Documentation**: [https://www.uvicorn.org/](https://www.uvicorn.org/)

---

## 🤝 API Support

### Need Help?
- Check the interactive docs at `/docs`
- Review the OpenAPI schema at `/openapi.json`
- Test endpoints directly in Swagger UI
- Run `python test_api.py` for automated tests

### Common Issues

**Q: API returns 503 Service Unavailable**  
A: Check that MongoDB is running and Ollama server is accessible

**Q: Natural language queries are slow**  
A: This is expected - Ollama LLM inference takes 2-10 seconds locally

**Q: CORS errors in browser**  
A: Ensure CORS middleware is properly configured in `api.py`

**Q: Movies not found**  
A: Run `python data_ingestion.py` to load the dataset

---

## 📄 License

This API is for educational purposes. The TMDB dataset is used under fair use for learning and demonstration.

---

**Built with ❤️ using FastAPI, LangChain, and Ollama**
