# TMDB Movie AI Agent - Frontend

> A modern, Netflix-inspired React application for exploring 50,000+ movies with AI-powered search and recommendations.

[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0.8-646CFF.svg)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)

A beautiful, responsive web interface that combines traditional search with cutting-edge AI assistance to help you discover movies. Built with React 18, Vite, and styled with a sleek Netflix-inspired dark theme.

## Demo

**Key Features at a Glance:**

- **Smart Search** - Find movies by title, director, actor, or genre instantly
- **AI Chat Assistant** - Ask questions in natural language ("Best sci-fi from the 2010s?")
- **Beautiful UI** - Netflix-inspired dark theme with smooth animations
- **Live Statistics** - Real-time database stats (50k+ movies, directors, genres)
- **Blazing Fast** - Vite HMR for instant updates during development
- **Fully Responsive** - Perfect on desktop, tablet, and mobile

## Features

### Advanced Movie Search

- **Multiple Search Modes**: Title, Director, Actor, Genre with instant switching
- **Advanced Filters**: Combine genre, year range (1900-2025), min rating, director, and actor
- **Smart Results**: Beautiful movie cards with posters, ratings, and metadata
- **Real-time Feedback**: Loading states and helpful error messages

### AI Assistant

- **Natural Language Queries**: Just ask like talking to a friend
- **Conversation History**: The AI remembers context within the chat
- **Quick Suggestions**: Pre-made queries to get you started
- **Rich Responses**: Formatted answers with movie lists and recommendations
- **Typing Indicators**: See when the AI is "thinking"

### Movie Display

- **High-Quality Posters**: TMDB poster images with fallback placeholders
- **Rich Metadata**: Title, year, rating, director, genres, runtime, overview
- **Color-Coded Ratings**: Green (7+), Orange (5-7), Red (<5)
- **Hover Effects**: Smooth animations and card elevation
- **Responsive Grid**: Adapts from 1 to 5 columns based on screen size

### Statistics Dashboard

- **Live Stats**: Total movies, directors, and genres in the header
- **Database Insights**: Access comprehensive movie database analytics
- **Visual Appeal**: Animated stats counter on load

## Technology Stack

### Core Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | Modern UI library with hooks and concurrent features |
| **Vite** | 5.0.8 | Lightning-fast build tool with HMR |
| **Axios** | 1.6.2 | Promise-based HTTP client for API calls |
| **React Icons** | 4.12.0 | Beautiful icon library (Font Awesome, Material, etc.) |

### Why These Technologies?

**React 18** - Latest React with improved performance and concurrent rendering  
**Vite** - 10-100x faster than traditional bundlers, instant HMR  
**Axios** - Better than fetch API with interceptors, auto-transform, and better error handling  
**CSS Variables** - Easy theming and consistent design system

## Prerequisites

Before you begin, ensure you have:

- **Node.js 16+** (18+ recommended) - [Download here](https://nodejs.org/)
- **npm** or **yarn** - Comes with Node.js
- **Backend API running** on `http://localhost:8000` - [Setup guide](../README.md)
- **MongoDB** with movie data loaded - See [Quick Start](../QUICKSTART.md)

**Quick Check:**

```bash
node --version  # Should be 16+
npm --version   # Should be 8+
```

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

**What gets installed:**

- React & React DOM (~500 KB)
- Vite & plugins (~10 MB)
- Axios (~200 KB)
- React Icons (~5 MB)
- Total: ~15 MB (node_modules will be ~200 MB with all deps)

### 2. Start Development Server

```bash
npm run dev
```

**Expected output:**

```
  VITE v5.0.8  ready in 342 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.x:3000/
  ➜  press h + enter to show help
```

Open `http://localhost:3000` in your browser!

### 3. Build for Production

```bash
npm run build
```

Production files will be in the `dist/` folder (~500 KB gzipped).

### 4. Preview Production Build

```bash
npm run preview
```

Test the production build locally before deployment.

## Full Stack Setup

To run the complete application:

**Terminal 1 - Backend API:**

```bash
# From project root
cd c:\Users\timot\Documents\GitHub\langchain_ollama
.venv\Scripts\Activate.ps1  # Activate venv (Windows)
uvicorn api:app --reload

# API will be available at http://localhost:8000
```

**Terminal 2 - Frontend:**

```bash
# From project root
cd frontend
npm run dev

# Frontend will be available at http://localhost:3000
```

**Terminal 3 - MongoDB (if not running as service):**

```bash
mongod --dbpath C:\data\db
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── MovieCard.jsx       # Individual movie card with poster
│   │   ├── MovieCard.css       # Card styling with hover effects
│   │   ├── MovieList.jsx       # Grid layout for movies
│   │   ├── MovieList.css       # Responsive grid styling
│   │   ├── MovieSearch.jsx     # Search interface with filters
│   │   ├── MovieSearch.css     # Search UI styling
│   │   ├── AIChat.jsx          # AI chat interface
│   │   └── AIChat.css          # Chat bubble styling
│   ├── services/
│   │   └── api.js              # Axios API client (all endpoints)
│   ├── App.jsx                 # Main app with routing & state
│   ├── App.css                 # App-level styling
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles & CSS variables
├── index.html               # HTML template
├── vite.config.js           # Vite config with proxy
├── package.json             # Dependencies & scripts
├── README.md                # This file
└── .gitignore               # Git ignore rules
```

## Usage

### Search Movies

**Simple Search:**

1. Select search type: **Title** / **Director** / **Actor** / **Genre**
2. Type your search query (e.g., "Batman", "Nolan", "DiCaprio")
3. Click **Search** or press Enter
4. Browse results in a beautiful grid

**Advanced Filters:**

1. Click **🔽 Advanced Filters** button
2. Combine multiple criteria:
   - **Genre**: Action, Drama, Comedy, Sci-Fi, etc.
   - **Year Range**: 1900 to 2025
   - **Min Rating**: 0.0 to 10.0
   - **Director**: Director name
   - **Actor**: Actor name
3. Click **Search** to apply filters
4. Click **Reset** to clear all filters

### AI Assistant

**Quick Start:**

1. Click the **🤖 AI Assistant** tab
2. Type a natural language question
3. Press Enter or click **Send**

**Example Queries:**

```
"Show me sci-fi movies from the 2010s"
"Find movies directed by Christopher Nolan"
"What are some highly rated action movies?"
"Recommend movies similar to Inception"
"Best movies of 2023"
"Movies with Tom Hanks"
"Action movies from the 90s"
```

**Pro Tips:**

- Use the **suggestion chips** for inspiration
- The AI remembers conversation context
- Responses include movie lists when relevant
- Click on the search tab to see full results

## Theming & Customization

The app uses **CSS Variables** for easy theming. All colors and spacing can be customized in [src/index.css](src/index.css):

```css
:root {
  /* Colors */
  --primary-color: #e50914;      /* Netflix red - CTAs, active states */
  --background: #141414;          /* Main dark background */
  --card-bg: #1f1f1f;            /* Card/component background */
  --secondary-color: #2a2a2a;    /* Input backgrounds */
  --border-color: #3a3a3a;       /* Borders and dividers */
  
  /* Text Colors */
  --text-primary: #ffffff;        /* Main text */
  --text-secondary: #b3b3b3;     /* Secondary text, labels */
  
  /* Status Colors */
  --success-color: #46d369;       /* High ratings (7+) */
  --warning-color: #ffa500;       /* Medium ratings (5-7) */
  --error-color: #ff4444;         /* Low ratings, errors */
  --hover-color: #333333;         /* Hover states */
}
```

**Creating Your Own Theme:**

1. **Blue Theme Example:**

```css
:root {
  --primary-color: #0066ff;
  --background: #0a0e27;
  --card-bg: #1a1f3a;
}
```

1. **Light Theme Example:**

```css
:root {
  --primary-color: #e50914;
  --background: #ffffff;
  --card-bg: #f5f5f5;
  --text-primary: #000000;
  --text-secondary: #666666;
}
```

## API Integration

### API Service Layer

All API calls are centralized in [src/services/api.js](src/services/api.js) using Axios:

```javascript
import movieAPI from './services/api';

// Search movies by title
const movies = await movieAPI.searchMovies('Inception');

// Get top rated movies
const topMovies = await movieAPI.getTopMovies(20);

// Get movies by director
const nolanMovies = await movieAPI.getMoviesByDirector('Christopher Nolan');

// Get movies by genre
const sciFiMovies = await movieAPI.getMoviesByGenre('Science Fiction');

// Get movies by year range
const nineties = await movieAPI.getMoviesByYearRange(1990, 1999);

// Get movies with actor
const hanksMovies = await movieAPI.getMoviesWithActor('Tom Hanks');

// Get database statistics
const stats = await movieAPI.getStatistics();

// Natural language AI query
const result = await movieAPI.queryAgent('best sci-fi movies');

// Health check
const health = await movieAPI.checkHealth();
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/movies/search?title=` | Search by title |
| GET | `/api/movies/top?limit=` | Top rated movies |
| GET | `/api/movies/director?name=` | Movies by director |
| GET | `/api/movies/genre?genre=` | Movies by genre |
| GET | `/api/movies/year-range?start=&end=` | Movies by year |
| GET | `/api/movies/actor?name=` | Movies with actor |
| GET | `/api/movies/statistics` | Database stats |
| POST | `/api/query` | AI natural language query |

### Error Handling

The API service includes automatic error handling:

```javascript
try {
  const movies = await movieAPI.searchMovies('Batman');
  console.log(movies);
} catch (error) {
  // Error is automatically formatted
  console.error(error.message);
}
```

## ⚙️ Configuration

### Vite Dev Server

Configure the dev server in [vite.config.js](vite.config.js):

```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,                    // Frontend port
    open: true,                    // Auto-open browser
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Backend URL
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
```

### Environment Variables

Create a `.env` file in the frontend folder:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000

# Optional: Custom port
VITE_PORT=3000
```

**Usage in code:**

```javascript
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### Build Configuration

Customize the production build:

```javascript
// vite.config.js
export default defineConfig({
  build: {
    outDir: 'dist',
    sourcemap: false,           // Disable for smaller bundle
    minify: 'terser',           // Better minification
    chunkSizeWarningLimit: 1000 // Warn on large chunks
  }
})
```

## Troubleshooting

### Common Issues & Solutions

#### API Connection Issues

**Problem:** `Network Error` or `ERR_CONNECTION_REFUSED`

**Solutions:**

1. Ensure backend is running: `uvicorn api:app --reload`
2. Check backend URL: Should be `http://localhost:8000`
3. Verify CORS is enabled in [api.py](../api.py):

   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

4. Check proxy config in [vite.config.js](vite.config.js)
5. Try accessing API directly: `http://localhost:8000/api/health`

#### Build Errors

**Problem:** `Module not found` or dependency errors

**Solution:**

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Or on Windows
rmdir /s /q node_modules
del package-lock.json
npm install
```

#### Port Already in Use

**Problem:** `Port 3000 is already in use`

**Solutions:**

1. Change port in vite.config.js:

```javascript
server: {
  port: 3001  // Use different port
}
```

1. **Kill process using port 3000:**

```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:3000 | xargs kill -9
```

#### ❌ Slow Performance

**Problem:** App is slow or laggy

**Solutions:**

1. ✅� Related

- 📖 [Backend API Documentation](../API_README.md) - REST API endpoints
- 🏗️ [Project Architecture](../ARCHITECTURE.md) - System design
- 🚀 [Quick Start Guide](../QUICKSTART.md) - 10-minute setup
- 📝 [Main README](../README.md) - Project overview
- 📊 [Project Summary](../Project_summary/PROJECT_SUMMARY.md) - Statistics & features

## 💬 Support

Need help? Here's how to get support:

### Common Issues

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Review [backend API logs](../api.py) for errors
3. Check MongoDB connection and data
4. Verify Ollama is running (`ollama list`)

### Getting Help

- **Issues**: Open a [GitHub Issue](../../issues)
- **Discussions**: Join [GitHub Discussions](../../discussions)
- **Documentation**: Read the [main README](../README.md)
- **Bug Reports**: Include browser, error message, and steps to reproduce

### Before Asking

- Check if backend API is running
- Look at browser console for errors (F12)
- Check Network tab for failed requests
- Try in incognito/private mode
- Clear browser cache

---

## 🎉 Acknowledgments

Built with amazing open-source technologies:

- [React](https://react.dev/) - UI library
- [Vite](https://vitejs.dev/) - Build tool
- [Axios](https://axios-http.com/) - HTTP client
- [React Icons](https://react-icons.github.io/react-icons/) - Icon library
- [TMDB](https://www.themoviedb.org/) - Movie database

## 📜 License

MIT License - See [LICENSE](../LICENSE) file for details

---

<div align="center">

**Built with React, Vite, and FastAPI**

Star this repo if you find it helpful!

[Home](../README.md) • [API Docs](../API_README.md) • [Quick Start](../QUICKSTART.md)

</div>

**Check:**

1. Backend API is running
2. Ollama is running: `ollama list`
3. Mistral model is available: `ollama pull mistral`
4. MongoDB has movie data: `python data_ingestion.py`
5. Check browser console for error messages

### Debug Mode

Enable detailed logging:

```javascript
// In src/services/api.js
apiClient.interceptors.request.use(request => {
  console.log('🚀 Request:', request);
  return request;
});

apiClient.interceptors.response.use(response => {
  console.log('✅ Response:', response);
  return response;
});
```

## Performance

### Bundle Size

```
dist/
├── index.html           2 KB
├── assets/
│   ├── index-[hash].js  180 KB (50 KB gzipped)
│   └── index-[hash].css 25 KB (5 KB gzipped)
└── Total:               ~55 KB gzipped 🎉
```

### Optimization Features

**Vite HMR** - Instant hot module replacement (<50ms)  
**Code Splitting** - Automatic route-based splitting  
**Lazy Loading** - Images load on scroll  
**Tree Shaking** - Unused code removed  
**Minification** - Terser for JS, cssnano for CSS  
**Compression** - Gzip/Brotli supported  

### Performance Tips

1. **Limit search results** - Use pagination or limit to 50 movies
2. **Debounce search input** - Wait 300ms before searching
3. **Cache API responses** - Store in localStorage for 5 minutes
4. **Optimize images** - Use TMDB's w300 instead of original
5. **Enable compression** - Configure your web server (nginx, Apache)

## Deployment

### Vercel (Recommended)

**One-click deployment:**

```bash
# Install Vercel CLI
npm i -g vercel

# Build and deploy
npm run build
vercel --prod
```

**vercel.json:**

```json
{
  "rewrites": [
    { "source": "/api/(.*)", "destination": "http://your-backend.com/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

### Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Build and deploy
npm run build
netlify deploy --prod --dir=dist
```

**netlify.toml:**

```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/api/*"
  to = "http://your-backend.com/api/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Docker

**Dockerfile:**

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**nginx.conf:**

```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    location /api/ {
        proxy_pass http://backend:8000/api/;
    }
}
```

**Build and run:**

```bash
docker build -t movie-frontend .
docker run -p 3000:80 movie-frontend
```

### Static Hosting (GitHub Pages, S3)

```bash
# Build
npm run build

# Upload dist/ folder to:
# - GitHub Pages
# - AWS S3 + CloudFront
# - Azure Static Web Apps
# - Google Cloud Storage
```

**Note:** You'll need to configure API proxy separately (use CORS from backend).

## Testing

### Manual Testing Checklist

- [ ] Search by title works
- [ ] Search by director works
- [ ] Search by actor works
- [ ] Search by genre dropdown works
- [ ] Advanced filters combine correctly
- [ ] AI chat responds to queries
- [ ] Movie cards display correctly
- [ ] Ratings show correct colors
- [ ] Mobile responsive (test on phone)
- [ ] Statistics load in header
- [ ] Error messages are helpful
- [ ] Loading states work

### Browser Testing

Tested on:

- Chrome 120+ (Recommended)
- Firefox 120+
- Safari 17+
- Edge 120+

## Tips & Tricks

### Developer Tips

1. **Fast Refresh** - Vite HMR preserves state during development
2. **React DevTools** - Install browser extension for debugging
3. **Network Tab** - Monitor API calls and response times
4. **Console Logs** - Check for errors (F12 → Console)
5. **Component Hierarchy** - Use React DevTools to inspect props/state

### Performance Tips

1. **Lazy load images** - Only load visible movie posters
2. **Debounce search** - Wait for user to stop typing
3. **Virtual scrolling** - For very long lists (100+ movies)
4. **Service Workers** - Cache static assets
5. **CDN** - Serve static files from CDN

### UI/UX Tips

1. **Keyboard shortcuts** - Add Ctrl+K for quick search
2. **Dark mode toggle** - Let users switch themes
3. **Favorites** - Save movies to localStorage
4. **Recently viewed** - Track viewing history
5. **Share button** - Share movie lists via URL

## Resources

### Official Documentation

- [React Docs](https://react.dev/) - React 18 documentation
- [Vite Guide](https://vitejs.dev/guide/) - Vite configuration guide
- [Axios Docs](https://axios-http.com/) - HTTP client documentation

### Learning Resources

- [React Tutorial](https://react.dev/learn) - Official React tutorial
- [Vite Features](https://vitejs.dev/guide/features.html) - Learn about Vite
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/--*) - Theming guide

### Related Projects

- [TMDB API](https://www.themoviedb.org/documentation/api) - Movie database API
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [LangChain](https://python.langchain.com/) - AI agent framework

## FAQ

**Q: Can I use TypeScript instead of JavaScript?**  
A: Yes! Run `npm install -D typescript @types/react @types/react-dom` and rename files to `.tsx`

**Q: How do I add user authentication?**  
A: Integrate with OAuth (Google, GitHub) or use JWT tokens with the backend API

**Q: Can I add more movie sources (Netflix, Amazon)?**  
A: Yes, extend the backend API to include additional data sources and update the frontend

**Q: How do I deploy to production?**  
A: See the [Deployment](#-deployment) section above for Vercel, Netlify, Docker options

**Q: Is there a mobile app?**  
A: Not yet, but the web app is fully responsive and works great on mobile browsers

**Q: Can I customize the theme?**  
A: Absolutely! See the [Theming](#-theming--customization) section

## Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Use **functional components** with hooks
- Follow **React best practices** (use keys, avoid index keys)
- Keep components **small and focused** (< 200 lines)
- Add **PropTypes** or TypeScript for type safety
- Use **CSS modules** or styled-components for scoped styles
- Write **meaningful commit messages**

## License

MIT License - See LICENSE file for details

## Related

- [Backend API Documentation](../API_README.md)
- [Project Architecture](../ARCHITECTURE.md)
- [Quick Start Guide](../QUICKSTART.md)

## Support

For issues or questions:

- Check the [main README](../README.md)
- Review backend API docs
- Check backend logs for API errors

---

Built with React, Vite, and FastAPI
