import React, { useState, useRef, useEffect } from 'react';
import { FaPaperPlane, FaRobot, FaUser } from 'react-icons/fa';
import './AIChat.css';

const AIChat = ({ onQuery }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Hi! I\'m your AI movie assistant. Ask me anything about movies! For example:\n\n• "Show me sci-fi movies from the 2010s"\n• "Find movies directed by Christopher Nolan"\n• "What are some highly rated action movies?"\n• "Recommend movies similar to Inception"'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await onQuery(userMessage);
      
      // Add assistant response
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: response.answer || response.message || 'No response received.',
        movies: response.movies || []
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: `❌ Error: ${error.message || 'Failed to get response from AI assistant.'}`,
        error: true
      }]);
    } finally {
      setLoading(false);
    }
  };

  const suggestions = [
    "Best movies of 2023",
    "Christopher Nolan movies",
    "High-rated sci-fi films",
    "Movies with Tom Hanks",
    "Action movies from the 90s"
  ];

  const handleSuggestionClick = (suggestion) => {
    setInput(suggestion);
  };

  return (
    <div className="ai-chat">
      <div className="chat-header">
        <FaRobot className="chat-icon" />
        <div>
          <h2>AI Movie Assistant</h2>
          <p>Ask questions in natural language</p>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'user' ? <FaUser /> : <FaRobot />}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
              {message.movies && message.movies.length > 0 && (
                <div className="message-movies">
                  <strong>Found {message.movies.length} movies:</strong>
                  <ul>
                    {message.movies.slice(0, 5).map((movie, i) => (
                      <li key={i}>
                        <strong>{movie.title}</strong> ({movie.year || 'N/A'})
                        {movie.vote_average && ` - Rating: ${movie.vote_average}/10`}
                      </li>
                    ))}
                  </ul>
                  {message.movies.length > 5 && (
                    <p className="more-movies">...and {message.movies.length - 5} more</p>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message assistant typing">
            <div className="message-avatar">
              <FaRobot />
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <div className="suggestions">
          <p className="suggestions-title">Try asking:</p>
          <div className="suggestion-chips">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-chip"
                onClick={() => handleSuggestionClick(suggestion)}
                disabled={loading}
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about movies... (e.g., 'sci-fi movies from 2020')"
          className="chat-input"
          disabled={loading}
        />
        <button 
          type="submit" 
          className="send-btn" 
          disabled={loading || !input.trim()}
        >
          <FaPaperPlane />
        </button>
      </form>
    </div>
  );
};

export default AIChat;
