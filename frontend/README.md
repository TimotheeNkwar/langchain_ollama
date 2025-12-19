# TMDB Movie AI Agent - Frontend

Modern React frontend for the TMDB Movie AI Agent, providing a beautiful web interface to explore 50,000+ movies with AI-powered search capabilities.

## 🎨 Features

- **🔍 Advanced Movie Search**: Search by title, director, actor, genre, year range, and rating
- **🤖 AI Assistant**: Natural language queries powered by LangChain & Ollama
- **🎬 Beautiful UI**: Netflix-inspired dark theme with responsive design
- **📊 Statistics Dashboard**: Real-time database statistics
- **⚡ Fast Performance**: Built with Vite for lightning-fast development
- **📱 Mobile Responsive**: Works seamlessly on all devices

## 🛠️ Technology Stack

- **React 18.2.0**: Modern UI library
- **Vite 5.0.8**: Next-generation frontend tooling
- **Axios 1.6.2**: HTTP client for API requests
- **React Icons 4.12.0**: Beautiful icon library
- **CSS3**: Custom styling with CSS variables

## 📦 Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running on `http://localhost:8000`

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

Production files will be in the `dist/` folder.

### 4. Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── MovieCard.jsx       # Movie card component
│   │   ├── MovieCard.css
│   │   ├── MovieList.jsx       # Movie grid display
│   │   ├── MovieList.css
│   │   ├── MovieSearch.jsx     # Search interface
│   │   ├── MovieSearch.css
│   │   ├── AIChat.jsx          # AI chat assistant
│   │   └── AIChat.css
│   ├── services/
│   │   └── api.js              # API service layer
│   ├── App.jsx                 # Main app component
│   ├── App.css
│   ├── main.jsx                # React entry point
│   └── index.css               # Global styles
├── index.html                  # HTML template
├── vite.config.js             # Vite configuration
└── package.json               # Dependencies
```

## 🎯 Usage

### Search Movies

1. **Simple Search**: Use the tab selector to choose search type (Title, Director, Actor, Genre)
2. **Advanced Filters**: Click "Advanced Filters" for multi-criteria search
3. **Results**: Movies appear in a responsive grid with ratings, posters, and details

### AI Assistant

1. Click the "AI Assistant" tab
2. Type natural language queries like:
   - "Show me sci-fi movies from the 2010s"
   - "Find movies directed by Christopher Nolan"
   - "What are some highly rated action movies?"
3. The AI will search and provide recommendations

## 🔧 Configuration

### API Proxy

The Vite dev server is configured to proxy API requests to the backend:

```javascript
// vite.config.js
export default {
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}
```

### Environment Variables

Create a `.env` file for custom configuration:

```bash
VITE_API_URL=http://localhost:8000
```

## 🎨 Theming

The app uses CSS variables for easy theming:

```css
:root {
  --primary-color: #e50914;      /* Netflix red */
  --background: #141414;          /* Dark background */
  --card-bg: #1f1f1f;            /* Card background */
  --text-primary: #ffffff;        /* Primary text */
  --text-secondary: #b3b3b3;     /* Secondary text */
}
```

## 📱 API Integration

All API calls are centralized in `src/services/api.js`:

```javascript
import movieAPI from './services/api';

// Search movies
const movies = await movieAPI.searchMovies('Inception');

// Get top rated movies
const topMovies = await movieAPI.getTopMovies(20);

// AI query
const result = await movieAPI.queryAgent('sci-fi movies');
```

## 🐛 Troubleshooting

### API Connection Issues

- Ensure the backend is running on `http://localhost:8000`
- Check CORS settings in backend `api.py`
- Verify the proxy configuration in `vite.config.js`

### Build Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

```bash
# Change port in vite.config.js
server: {
  port: 3001  // Use different port
}
```

## 📊 Performance

- **Vite HMR**: Instant hot module replacement
- **Code Splitting**: Automatic route-based splitting
- **Lazy Loading**: Images load on demand
- **Optimized Bundle**: Production build is minified and optimized

## 🚢 Deployment

### Vercel

```bash
npm run build
vercel --prod
```

### Netlify

```bash
npm run build
netlify deploy --prod --dir=dist
```

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "run", "preview"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Related

- [Backend API Documentation](../API_README.md)
- [Project Architecture](../ARCHITECTURE.md)
- [Quick Start Guide](../QUICKSTART.md)

## 💬 Support

For issues or questions:
- Check the [main README](../README.md)
- Review backend API docs
- Check backend logs for API errors

---

Built with ❤️ using React, Vite, and FastAPI
