import React, { useState } from 'react';
import { FaSearch, FaFilter } from 'react-icons/fa';
import './MovieSearch.css';

const MovieSearch = ({ onSearch, loading }) => {
  const [searchType, setSearchType] = useState('title');
  const [searchValue, setSearchValue] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [advancedFilters, setAdvancedFilters] = useState({
    genre: '',
    yearFrom: '',
    yearTo: '',
    director: '',
    actor: '',
    minRating: ''
  });

  const handleSimpleSearch = (e) => {
    e.preventDefault();
    if (searchValue.trim()) {
      onSearch(searchType, searchValue.trim());
    }
  };

  const handleAdvancedSearch = (e) => {
    e.preventDefault();
    onSearch('advanced', advancedFilters);
  };

  const handleReset = () => {
    setSearchValue('');
    setAdvancedFilters({
      genre: '',
      yearFrom: '',
      yearTo: '',
      director: '',
      actor: '',
      minRating: ''
    });
  };

  const genres = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
    'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
    'Romance', 'Science Fiction', 'Thriller', 'War', 'Western'
  ];

  return (
    <div className="movie-search">
      {/* Simple Search */}
      <div className="search-header">
        <h2>🎬 Movie Search</h2>
        <button 
          className="toggle-advanced-btn"
          onClick={() => setShowAdvanced(!showAdvanced)}
          type="button"
        >
          <FaFilter /> {showAdvanced ? 'Simple Search' : 'Advanced Filters'}
        </button>
      </div>

      {!showAdvanced ? (
        <form onSubmit={handleSimpleSearch} className="simple-search">
          <div className="search-type-selector">
            <button
              type="button"
              className={searchType === 'title' ? 'active' : ''}
              onClick={() => setSearchType('title')}
            >
              Title
            </button>
            <button
              type="button"
              className={searchType === 'director' ? 'active' : ''}
              onClick={() => setSearchType('director')}
            >
              Director
            </button>
            <button
              type="button"
              className={searchType === 'actor' ? 'active' : ''}
              onClick={() => setSearchType('actor')}
            >
              Actor
            </button>
            <button
              type="button"
              className={searchType === 'genre' ? 'active' : ''}
              onClick={() => setSearchType('genre')}
            >
              Genre
            </button>
          </div>

          <div className="search-input-group">
            {searchType === 'genre' ? (
              <select
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                className="search-select"
                disabled={loading}
              >
                <option value="">Select a genre...</option>
                {genres.map(genre => (
                  <option key={genre} value={genre}>{genre}</option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={searchValue}
                onChange={(e) => setSearchValue(e.target.value)}
                placeholder={`Search by ${searchType}...`}
                className="search-input"
                disabled={loading}
              />
            )}
            <button type="submit" className="search-btn" disabled={loading || !searchValue}>
              <FaSearch /> Search
            </button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleAdvancedSearch} className="advanced-search">
          <div className="filter-grid">
            <div className="filter-group">
              <label>Genre</label>
              <select
                value={advancedFilters.genre}
                onChange={(e) => setAdvancedFilters({...advancedFilters, genre: e.target.value})}
                disabled={loading}
              >
                <option value="">Any Genre</option>
                {genres.map(genre => (
                  <option key={genre} value={genre}>{genre}</option>
                ))}
              </select>
            </div>

            <div className="filter-group">
              <label>Year From</label>
              <input
                type="number"
                value={advancedFilters.yearFrom}
                onChange={(e) => setAdvancedFilters({...advancedFilters, yearFrom: e.target.value})}
                placeholder="1900"
                min="1900"
                max={new Date().getFullYear()}
                disabled={loading}
              />
            </div>

            <div className="filter-group">
              <label>Year To</label>
              <input
                type="number"
                value={advancedFilters.yearTo}
                onChange={(e) => setAdvancedFilters({...advancedFilters, yearTo: e.target.value})}
                placeholder={new Date().getFullYear()}
                min="1900"
                max={new Date().getFullYear()}
                disabled={loading}
              />
            </div>

            <div className="filter-group">
              <label>Min Rating</label>
              <input
                type="number"
                value={advancedFilters.minRating}
                onChange={(e) => setAdvancedFilters({...advancedFilters, minRating: e.target.value})}
                placeholder="0.0"
                min="0"
                max="10"
                step="0.1"
                disabled={loading}
              />
            </div>

            <div className="filter-group">
              <label>Director</label>
              <input
                type="text"
                value={advancedFilters.director}
                onChange={(e) => setAdvancedFilters({...advancedFilters, director: e.target.value})}
                placeholder="Director name..."
                disabled={loading}
              />
            </div>

            <div className="filter-group">
              <label>Actor</label>
              <input
                type="text"
                value={advancedFilters.actor}
                onChange={(e) => setAdvancedFilters({...advancedFilters, actor: e.target.value})}
                placeholder="Actor name..."
                disabled={loading}
              />
            </div>
          </div>

          <div className="filter-actions">
            <button type="button" onClick={handleReset} className="reset-btn" disabled={loading}>
              Reset
            </button>
            <button type="submit" className="search-btn" disabled={loading}>
              <FaSearch /> Search
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default MovieSearch;
