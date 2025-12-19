import React from 'react';
import MovieCard from './MovieCard';
import './MovieList.css';

const MovieList = ({ movies, loading, error }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Loading movies...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-message">❌ {error}</p>
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <div className="empty-container">
        <p className="empty-message">🎬 No movies found. Try a different search!</p>
      </div>
    );
  }

  return (
    <div className="movie-list">
      <div className="movie-grid">
        {movies.map((movie, index) => (
          <MovieCard key={movie.tmdb_id || movie.imdb_id || index} movie={movie} />
        ))}
      </div>
    </div>
  );
};

export default MovieList;
