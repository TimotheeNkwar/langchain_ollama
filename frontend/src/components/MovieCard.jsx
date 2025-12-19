import React from 'react';
import { FaStar, FaCalendar, FaFilm } from 'react-icons/fa';
import './MovieCard.css';

const MovieCard = ({ movie }) => {
  const {
    title,
    year,
    vote_average,
    overview,
    genres,
    director,
    poster_path,
    runtime_minutes
  } = movie;

  const posterUrl = poster_path 
    ? `https://image.tmdb.org/t/p/w500${poster_path}`
    : '/placeholder-movie.png';

  const rating = vote_average ? parseFloat(vote_average).toFixed(1) : 'N/A';
  const ratingColor = vote_average >= 7 ? '#46d369' : vote_average >= 5 ? '#ffa500' : '#ff4444';

  return (
    <div className="movie-card">
      <div className="movie-poster">
        <img src={posterUrl} alt={title} onError={(e) => {
          e.target.src = 'https://via.placeholder.com/300x450/1f1f1f/ffffff?text=No+Poster';
        }} />
        <div className="movie-rating" style={{ backgroundColor: ratingColor }}>
          <FaStar /> {rating}
        </div>
      </div>
      
      <div className="movie-info">
        <h3 className="movie-title">{title}</h3>
        
        <div className="movie-meta">
          {year && (
            <span className="meta-item">
              <FaCalendar /> {year}
            </span>
          )}
          {runtime_minutes && (
            <span className="meta-item">
              <FaFilm /> {runtime_minutes} min
            </span>
          )}
        </div>

        {director && (
          <p className="movie-director">
            <strong>Director:</strong> {director}
          </p>
        )}

        {genres && (
          <div className="movie-genres">
            {genres.split(',').slice(0, 3).map((genre, index) => (
              <span key={index} className="genre-tag">
                {genre.trim()}
              </span>
            ))}
          </div>
        )}

        {overview && (
          <p className="movie-overview">
            {overview.length > 150 ? `${overview.substring(0, 150)}...` : overview}
          </p>
        )}
      </div>
    </div>
  );
};

export default MovieCard;
