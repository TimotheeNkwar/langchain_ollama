import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const movieAPI = {
  // Health check
  checkHealth: async () => {
    const response = await apiClient.get('/api/health');
    return response.data;
  },

  // Search movies by title
  searchMovies: async (title) => {
    const response = await apiClient.get('/api/movies/search', {
      params: { title }
    });
    return response.data;
  },

  // Get top rated movies
  getTopMovies: async (limit = 10) => {
    const response = await apiClient.get('/api/movies/top', {
      params: { limit }
    });
    return response.data;
  },

  // Get movies by director
  getMoviesByDirector: async (name) => {
    const response = await apiClient.get('/api/movies/director', {
      params: { name }
    });
    return response.data;
  },

  // Get movies by genre
  getMoviesByGenre: async (genre) => {
    const response = await apiClient.get('/api/movies/genre', {
      params: { genre }
    });
    return response.data;
  },

  // Get movies by year range
  getMoviesByYearRange: async (start, end) => {
    const response = await apiClient.get('/api/movies/year-range', {
      params: { start, end }
    });
    return response.data;
  },

  // Get movies with actor
  getMoviesWithActor: async (name) => {
    const response = await apiClient.get('/api/movies/actor', {
      params: { name }
    });
    return response.data;
  },

  // Get database statistics
  getStatistics: async () => {
    const response = await apiClient.get('/api/movies/statistics');
    return response.data;
  },

  // Natural language query (AI Agent)
  queryAgent: async (query) => {
    const response = await apiClient.post('/api/query', { question: query });
    return response.data;
  },
};

export default movieAPI;
