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
│                      main.py                                 │
│                 (CLI Interface)                              │
│  • User input handling                                       │
│  • Response formatting                                       │
│  • Session management                                        │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Query
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   movie_agent.py                             │
│                  (LangChain Agent)                           │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │         OpenAI GPT-3.5-turbo                 │          │
│  │    (Intent Understanding & Planning)         │          │
│  └──────────────────┬───────────────────────────┘          │
│                     │                                        │
│                     │ Tool Selection                         │
│                     ▼                                        │
│  ┌──────────────────────────────────────────────┐          │
│  │           Tool Executor                      │          │
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
└────────────────────────┬────────────────────────────────────┘
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
OpenAI GPT (Understand intent)
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

### 1. Agent Pattern
- **LangChain Agent**: Autonomous decision-making
- **Tool-based Architecture**: Modular, extensible tools
- **Function Calling**: GPT selects appropriate tools

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
- **LangChain**: Agent framework
- **OpenAI GPT-3.5**: Language model
- **MongoDB**: NoSQL database
- **PyMongo**: MongoDB driver

### Key Libraries
- `langchain`: Agent orchestration
- `langchain-openai`: OpenAI integration
- `pymongo`: Database connectivity
- `pandas`: Data processing
- `python-dotenv`: Environment management

## Scalability Considerations

### Current Implementation
- **Single-threaded**: One query at a time
- **Local/Cloud MongoDB**: Flexible deployment
- **Rate limits**: OpenAI API limits apply

### Future Enhancements
- **Caching**: Redis for frequent queries
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
- **API key rotation**: Regular key updates
- **Rate limiting**: Prevent abuse
- **Audit logging**: Track all queries

## Extension Points

### Adding New Tools
```python
# In movie_agent.py
Tool(
    name="your_tool_name",
    func=self.db_tools.your_function,
    description="When to use this tool"
)
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
# Modify prompt in movie_agent.py
self.prompt = ChatPromptTemplate.from_messages([
    ("system", "Your custom system prompt"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
```

## Performance Metrics

### Query Performance
- **Simple queries**: < 1 second
- **Complex aggregations**: 1-3 seconds
- **Agent reasoning**: 2-5 seconds (OpenAI API)

### Optimization Strategies
1. **Indexes**: Pre-created on common fields
2. **Projection**: Return only needed fields
3. **Limits**: Cap result sets
4. **Caching**: Store frequent queries

## Error Handling

### Layers
1. **MongoDB**: Connection and query errors
2. **OpenAI API**: Rate limits, authentication
3. **Agent**: Parsing and execution errors
4. **User Interface**: Input validation

### Recovery Strategies
- **Retry logic**: Transient failures
- **Fallback responses**: Graceful degradation
- **Error messages**: User-friendly explanations
- **Logging**: Debug information

---

This architecture provides a solid foundation for an AI-powered movie recommendation system with room for growth and enhancement.
