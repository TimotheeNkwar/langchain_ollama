# 🚀 Quick Start Guide

Get your TMDB Movie AI Agent running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Install and Start Ollama

1. Download Ollama from [ollama.ai](https://ollama.ai)

2. Install and start Ollama

3. Pull a model (choose one):
   ```bash
   ollama pull mistral
   # or
   ollama pull llama3.2
   # or
   ollama pull llama3.1
   # or
   ollama pull qwen2.5
   ```

4. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Step 3: Setup Environment

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and configure:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=mistral
   ```

3. Configure MongoDB (choose one):
   - **Local**: Keep default `MONGODB_URI=mongodb://localhost:27017/`
   - **Atlas**: Use your connection string

## Step 4: Start MongoDB

**Windows (Local):**
```bash
net start MongoDB
```

**MongoDB Atlas:**
- Already running in the cloud!

## Step 5: Load Data

```bash
python data_ingestion.py
```

This will load 5,000 movies from the TMDB dataset in batches.
Wait for "Data ingestion complete!" message (~30 seconds).

## Step 6: Run the Agent

```bash
python main.py
```

## Try These Queries

```
What are the top 10 rated movies?
Show me Christopher Nolan movies
Find action movies from the 2000s
What movies has Tom Hanks been in?
Search for Marvel movies
Find sci-fi movies with high ratings
```

## Troubleshooting

**Ollama not running?**
- Check if Ollama is running: `ollama list`
- Restart Ollama service
- Verify URL: `http://localhost:11434`

**Model not found?**
- Pull the model: `ollama pull mistral`
- Check available models: `ollama list`
- Update `OLLAMA_MODEL` in `.env`

**MongoDB not running?**
- Windows: `net start MongoDB`
- Check Task Manager for `mongod.exe`

**No movies found?**
- Run `python data_ingestion.py` again
- Check MongoDB connection
- Verify dataset file exists: `dataset/TMDB_movie_dataset_v11.csv`

**Data ingestion taking too long?**
- Should only take ~30 seconds for 5,000 movies
- Progress is shown during insertion
- Don't interrupt the process

---

That's it! You're ready to explore 5,000 movies with AI! 🎬
