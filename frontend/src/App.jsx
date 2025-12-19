import React, { useState, useEffect } from 'react';
import { FaFilm, FaGithub } from 'react-icons/fa';
import MovieSearch from './components/MovieSearch';
import MovieList from './components/MovieList';
import AIChat from './components/AIChat';
import movieAPI from './services/api';
import './App.css';

function App() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('search');
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Load top movies on mount
    loadTopMovies();
    // Load statistics
    loadStatistics();
  }, []);

  const loadTopMovies = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await movieAPI.getTopMovies(20);
      setMovies(data.movies || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const data = await movieAPI.getStatistics();
      setStats(data);
    } catch (err) {
      console.error('Failed to load statistics:', err);
    }
  };

  const handleSearch = async (searchType, searchValue) => {
    try {
      setLoading(true);
      setError(null);
      let data;

      if (searchType === 'advanced') {
        // Advanced search with multiple filters
        const params = {};
        if (searchValue.genre) params.genre = searchValue.genre;
        if (searchValue.yearFrom && searchValue.yearTo) {
          params.year_from = searchValue.yearFrom;
          params.year_to = searchValue.yearTo;
        }
        if (searchValue.minRating) params.min_rating = parseFloat(searchValue.minRating);
        
        // For now, use genre or year range search
        if (params.genre) {
          data = await movieAPI.getMoviesByGenre(params.genre);
        } else if (params.year_from && params.year_to) {
          data = await movieAPI.getMoviesByYearRange(params.year_from, params.year_to);
        } else {
          data = await movieAPI.getTopMovies(20);
        }
      } else {
        switch (searchType) {
          case 'title':
            data = await movieAPI.searchMovies(searchValue);
            break;
          case 'director':
            data = await movieAPI.getMoviesByDirector(searchValue);
            break;
          case 'actor':
            data = await movieAPI.getMoviesWithActor(searchValue);
            break;
          case 'genre':
            data = await movieAPI.getMoviesByGenre(searchValue);
            break;
          default:
            data = await movieAPI.searchMovies(searchValue);
        }
      }

      setMovies(data.movies || []);
      if (data.movies && data.movies.length === 0) {
        setError('No movies found matching your criteria.');
      }
    } catch (err) {
      setError(err.message);
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAIQuery = async (query) => {
    try {
      const data = await movieAPI.queryAgent(query);
      
      // If the response includes movies, display them
      if (data.movies && data.movies.length > 0) {
        setMovies(data.movies);
        setActiveTab('search'); // Switch to search tab to show results
      }
      
      return data;
    } catch (err) {
      throw new Error(err.message);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <FaFilm className="logo-icon" />
            <div>
              <h1>TMDB Movie AI Agent</h1>
              <p>Explore 50,000+ movies with AI-powered search</p>
            </div>
          </div>
          {stats && (
            <div className="header-stats">
              <div className="stat">
                <span className="stat-value">{stats.total_movies?.toLocaleString()}</span>
                <span className="stat-label">Movies</span>
              </div>
              <div className="stat">
                <span className="stat-value">{stats.total_directors?.toLocaleString()}</span>
                <span className="stat-label">Directors</span>
              </div>
              <div className="stat">
                <span className="stat-value">{stats.genres?.length || 0}</span>
                <span className="stat-label">Genres</span>
              </div>
            </div>
          )}
        </div>
      </header>

      <div className="tab-navigation">
        <button
          className={`tab-btn ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          🔍 Search Movies
        </button>
        <button
          className={`tab-btn ${activeTab === 'ai' ? 'active' : ''}`}
          onClick={() => setActiveTab('ai')}
        >
          🤖 AI Assistant
        </button>
      </div>

      <main className="app-main">
        <div className="container">
          {activeTab === 'search' ? (
            <>
              <MovieSearch onSearch={handleSearch} loading={loading} />
              <div className="results-header">
                <h2>
                  {movies.length > 0 
                    ? `${movies.length} Movie${movies.length !== 1 ? 's' : ''} Found`
                    : 'Top Rated Movies'}
                </h2>
              </div>
              <MovieList movies={movies} loading={loading} error={error} />
            </>
          ) : (
            <AIChat onQuery={handleAIQuery} />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="container">
          <p>
            Built with FastAPI, LangChain, Ollama & React | 
            <a 
              href="https://github.com/TimotheeNkwar/langchain_ollama" 
              target="_blank" 
              rel="noopener noreferrer"
              className="footer-link"
            >
              <FaGithub /> GitHub
            </a>
          </p>
          <p className="footer-note">
            Movie data from TMDB (The Movie Database) - 50,000+ movies
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
