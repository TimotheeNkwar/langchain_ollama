# 🎬 IMDB Movie AI Agent - API Documentation

API Flask REST pour interroger la base de données de films via l'agent IA.

## 🚀 Installation

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement**
Assurez-vous que votre fichier `.env` contient :
```env
MONGODB_URI=your_mongodb_connection_string
MONGODB_DATABASE=your_database_name
MONGODB_COLLECTION=your_collection_name
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral
```

3. **Démarrer le serveur**
```bash
python api.py
```

L'API sera accessible sur `http://localhost:5000`

## 📖 Endpoints

### 1. **GET /** - Documentation de l'API
Retourne la liste de tous les endpoints disponibles.

**Exemple :**
```bash
curl http://localhost:5000/
```

### 2. **GET /api/health** - Vérification de l'état
Vérifie que l'API et la base de données sont opérationnelles.

**Exemple :**
```bash
curl http://localhost:5000/api/health
```

**Réponse :**
```json
{
  "status": "healthy",
  "database": "connected",
  "agent": "ready"
}
```

### 3. **GET /api/movies/search** - Recherche par titre
Recherche des films par titre (partiel, insensible à la casse).

**Paramètres :**
- `title` (requis) : Titre ou fragment de titre

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/search?title=batman"
```

**Réponse :**
```json
[
  {
    "title": "The Dark Knight",
    "year": 2008,
    "imdb_rating": 9.0,
    "director": "Christopher Nolan",
    "genre": "Action, Crime, Drama"
  }
]
```

### 4. **GET /api/movies/top** - Top films
Retourne les films les mieux notés.

**Paramètres :**
- `limit` (optionnel, défaut: 10) : Nombre de films à retourner

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/top?limit=5"
```

### 5. **GET /api/movies/director** - Films par réalisateur
Recherche les films d'un réalisateur spécifique.

**Paramètres :**
- `name` (requis) : Nom du réalisateur

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/director?name=nolan"
```

### 6. **GET /api/movies/genre** - Films par genre
Recherche les films par genre.

**Paramètres :**
- `genre` (requis) : Genre du film (Action, Drama, Comedy, etc.)

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/genre?genre=action"
```

### 7. **GET /api/movies/year-range** - Films par période
Recherche les films dans une plage d'années.

**Paramètres :**
- `start` (requis) : Année de début
- `end` (requis) : Année de fin

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/year-range?start=1990&end=2000"
```

### 8. **GET /api/movies/actor** - Films avec acteur
Recherche les films avec un acteur spécifique.

**Paramètres :**
- `name` (requis) : Nom de l'acteur

**Exemple :**
```bash
curl "http://localhost:5000/api/movies/actor?name=dicaprio"
```

### 9. **GET /api/movies/statistics** - Statistiques
Retourne des statistiques sur la base de données.

**Exemple :**
```bash
curl http://localhost:5000/api/movies/statistics
```

**Réponse :**
```json
{
  "total_movies": 5000,
  "average_rating": 7.2,
  "year_range": {
    "earliest": 1920,
    "latest": 2024
  },
  "top_directors": [...]
}
```

### 10. **POST /api/query** - Requête en langage naturel
Interroge l'agent IA avec une question en langage naturel.

**Body (JSON) :**
```json
{
  "question": "What are the best movies from the 1990s?"
}
```

**Exemple :**
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 3 Christopher Nolan movies?"}'
```

**Réponse :**
```json
{
  "question": "What are the top 3 Christopher Nolan movies?",
  "answer": "Based on the database, the top 3 Christopher Nolan movies are..."
}
```

## 🧪 Tests

Un script de test est fourni pour tester tous les endpoints :

```bash
# Démarrer l'API dans un terminal
python api.py

# Dans un autre terminal, exécuter les tests
python test_api.py
```

## 🌐 Utilisation avec JavaScript/Frontend

### Exemple avec Fetch API :

```javascript
// Recherche de films
fetch('http://localhost:5000/api/movies/search?title=batman')
  .then(response => response.json())
  .then(data => console.log(data));

// Requête en langage naturel
fetch('http://localhost:5000/api/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: 'What are the best sci-fi movies?'
  })
})
  .then(response => response.json())
  .then(data => console.log(data.answer));
```

### Exemple avec Axios :

```javascript
import axios from 'axios';

// Recherche de films
const movies = await axios.get('http://localhost:5000/api/movies/search', {
  params: { title: 'batman' }
});

// Requête en langage naturel
const response = await axios.post('http://localhost:5000/api/query', {
  question: 'What are the best sci-fi movies?'
});
console.log(response.data.answer);
```

## 🔧 Configuration

### Mode Debug
Par défaut, l'API s'exécute en mode debug. Pour la production, modifiez `api.py` :

```python
app.run(
    host='0.0.0.0',
    port=5000,
    debug=False  # Désactiver pour la production
)
```

### CORS
Si vous accédez à l'API depuis un domaine différent, CORS est inclus via `flask-cors` (installé automatiquement).

Pour configurer CORS, modifiez `api.py` :

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Activer CORS pour tous les domaines
```

## 📝 Gestion des erreurs

L'API retourne des codes d'erreur HTTP standard :

- **200** : Succès
- **400** : Paramètres manquants ou invalides
- **404** : Endpoint non trouvé
- **500** : Erreur serveur
- **503** : Service indisponible (problème de connexion)

**Exemple de réponse d'erreur :**
```json
{
  "error": "Missing required parameter: title"
}
```

## 🚀 Déploiement

Pour déployer en production, considérez :

1. **Utiliser un serveur WSGI** comme Gunicorn :
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

2. **Utiliser un reverse proxy** comme Nginx

3. **Configurer HTTPS** pour la sécurité

4. **Utiliser des variables d'environnement** pour les configurations sensibles

## 💡 Conseils

- L'agent est initialisé une seule fois (singleton) pour optimiser les performances
- Les connexions MongoDB sont gérées automatiquement
- Le mode verbose de l'agent est désactivé pour des réponses propres
- Utilisez `/api/query` pour des requêtes complexes nécessitant le raisonnement de l'IA

## 📚 Ressources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
