# 🏗️ Architecture Overview

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Command Line)                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Natural Language Query
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   main.py / api.py                           │
│            (CLI Interface / REST API)                        │
│  • User input handling                                       │
│  • Response formatting                                       │
│  • Session management                                        │
│  • FastAPI endpoints (port 8000)                             │
│  • OpenAPI docs at /docs                                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Query
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     agent.py                                 │
│                  (LangChain Agent)                           │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │         Ollama (Local LLM)                   │          │
│  │  (mistral/llama3.2/llama3.1/qwen2.5)        │          │
│  │    (Intent Understanding & Planning)         │          │
│  └──────────────────┬───────────────────────────┘          │
│                     │                                        │
│                     │ Tool Selection                         │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────┐          │
│  │      Tool Executor (8 tools)                 │          │
│  │  • search_movies_by_title                    │          │
│  │  • get_movies_by_director                    │          │
│  │  • get_top_rated_movies                      │          │
│  │  • get_movies_by_genre                       │          │
│  │  • get_movies_by_year_range                  │          │
│  │  • get_movies_with_actor                     │          │
│  │  • get_movie_statistics                      │          │
│  │  • advanced_search                           │          │
│  └──────────────────┬───────────────────────────┘          │
└────────────────────┬┴────────────────────────────────────────┘
                     │
                     │ MongoDB Query
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  MovieDatabaseTools                          │
│              (Database Query Layer)                          │
│  • Query construction                                        │
│  • Result formatting                                         │
│  • Error handling                                            │
│  • Redis caching (automatic)                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                    ┌────┴────┐
                    │         │
                    ▼         ▼
          ┌─────────────┐  ┌──────────┐
          │ Redis Cache │  │ MongoDB  │
          │  (Fallback) │  │ Database │
          └─────────────┘  └──────────┘
                         │
                         │ PyMongo
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     MongoDB                                  │
│                  (Data Storage)                              │
│                                                              │
│  Database: imdb_movies                                       │
│  Collection: movies                                          │
│                                                              │
│  Indexes:                                                    │
│  • title                                                     │
│  • year                                                      │
│  • imdb_rating                                               │
│  • director                                                  │
│  • genre                                                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initial Setup (One-time)

```
CSV File → data_ingestion.py → MongoDB
                                  ↓
                           Create Indexes
                                  ↓
                           Ready for Queries
```

### 2. Query Processing (Runtime)

```
User Query
    ↓
main.py (Receive input)
    ↓
MovieAgent (LangChain)
    ↓
Ollama LLM (Understand intent)
    ↓
Tool Selection (Choose appropriate database tool)
    ↓
MovieDatabaseTools (Execute MongoDB query)
    ↓
MongoDB (Return results)
    ↓
MovieAgent (Format response)
    ↓
main.py (Display to user)
```

## Key Design Patterns

### 1. Agent Pattern (LangChain 1.0+)
- **create_agent API**: Simplified agent creation
- **Tool-based Architecture**: Modular, extensible 8 tools
- **Automatic Tool Selection**: LLM autonomously chooses tools
- **Message-based Invocation**: Modern message passing pattern

### 2. Repository Pattern
- **MovieDatabaseTools**: Abstracts database operations
- **Clean separation**: Business logic vs. data access
- **Reusable queries**: Standardized database operations

### 3. Dependency Injection
- **Environment variables**: Configuration management
- **Loose coupling**: Easy to swap implementations
- **Testability**: Mock database for testing

## Technology Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **LangChain 1.0+**: Agent framework with create_agent API
- **Ollama**: Local LLM server (mistral, llama3.2, llama3.1, qwen2.5)
- **FastAPI 0.125.0**: Modern REST API framework
- **MongoDB**: NoSQL database
- **PyMongo**: MongoDB driver
- **Redis 5.0+**: In-memory cache for query optimization

### Key Libraries
- `langchain>=1.0.0`: Agent orchestration
- `langchain-ollama>=1.0.0`: Ollama integration
- `fastapi>=0.109.0`: REST API framework
- `uvicorn[standard]>=0.27.0`: ASGI server
- `pymongo`: Database connectivity
- `pandas`: Data processing
- `python-dotenv`: Environment management
- `loguru>=0.7.2`: Advanced logging with rotation and retention
- `redis>=5.0.0`: Query caching and performance optimization

## Scalability Considerations

### Current Implementation
- **Single-threaded**: One query at a time
- **Local/Cloud MongoDB**: Flexible deployment
- **Local LLM**: No external API rate limits
- **Ollama Server**: Runs locally (http://localhost:11434)

### Future Enhancements
- ~~**Caching**: Redis for frequent queries~~ ✅ **IMPLEMENTED**
- **Connection pooling**: Better MongoDB performance
- **Async operations**: Handle concurrent requests
- **Vector search**: Semantic similarity search
- **Load balancing**: Multiple agent instances

## Security Architecture

### Current Measures
- **Environment variables**: Secrets not in code
- **Input validation**: Query sanitization
- **Error handling**: No sensitive data in errors
- **Read-only operations**: No data modification

### Production Recommendations
- **Authentication**: User authentication system
- **Authorization**: Role-based access control
- **Encryption**: TLS for MongoDB connections
- **Ollama Security**: Secure Ollama server access
- **Rate limiting**: Prevent abuse
- **Audit logging**: Track all queries

## Extension Points

### Adding New Tools
```python
# In agent.py - add to self.tools list
Tool(
    name="your_tool_name",
    func=lambda x: self.db_tools.your_function(self.clean_input(x)),
    description="When to use this tool - be specific for LLM understanding"
)

# Then agent will automatically have access to the new tool
```

### Adding New Data Sources
```python
# Create new database tools class
class NewDataSource:
    def __init__(self):
        # Initialize connection
        pass
    
    def query_method(self, params):
        # Query logic
        pass
```

### Custom Agent Behavior
```python
# Modify system_prompt in agent.py
system_prompt = """Your custom instructions for the agent.

Describe the tools and when to use them.
Provide clear guidelines for the agent's behavior."""

self.agent = create_agent(
    model=self.llm,
    tools=self.tools,
    system_prompt=system_prompt
)
```

## Performance Metrics

### Query Performance
- **Simple queries**: < 1 second
- **Complex aggregations**: 1-3 seconds
- **Agent reasoning**: 2-10 seconds (Ollama local inference)

### Optimization Strategies
1. **Indexes**: Pre-created on common fields
2. **Projection**: Return only needed fields
3. **Limits**: Cap result sets
4. **Redis Caching**: Automatic caching with TTL (30min-1hr)
   - Title search: 30 minutes TTL
   - Director/Genre/Actor: 1 hour TTL
   - Cache stats: `/api/cache/stats`
   - Graceful fallback if Redis unavailable

## Error Handling

### Layers
1. **MongoDB**: Connection and query errors
2. **Ollama Server**: Connection, model availability
3. **Agent**: Parsing and execution errors
4. **User Interface**: Input validation

## Logging Architecture

### Loguru Implementation
The application uses **loguru** for centralized, production-ready logging:

**Configuration:**
- **agent.log**: Agent operations, LLM interactions, tool selection
- **api.log**: API requests, responses, server lifecycle
- **main.log**: CLI interactions, user queries, errors

**Features:**
- Automatic rotation: 10 MB per file
- Retention policy: 7 days
- Rich format: `{time} | {level} | {name}:{function}:{line} - {message}`
- Backtrace enabled: Full stack traces for debugging
- Dual output: File + colorized console (INFO+)
- Levels: DEBUG, INFO, WARNING, ERROR automatically categorized

### Recovery Strategies
- **Retry logic**: Transient failures
- **Fallback responses**: Graceful degradation
- **Error messages**: User-friendly explanations
- **Logging**: Debug information

---

This architecture provides a solid foundation for an AI-powered movie recommendation system with room for growth and enhancement.
