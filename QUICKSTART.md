# 🚀 Quick Start Guide

Get your AI Movie Agent running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Setup Environment

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Configure MongoDB (choose one):
   - **Local**: Keep default `MONGODB_URI=mongodb://localhost:27017/`
   - **Atlas**: Use your connection string

## Step 3: Start MongoDB

**Windows (Local):**
```bash
net start MongoDB
```

**MongoDB Atlas:**
- Already running in the cloud!

## Step 4: Load Data

```bash
python data_ingestion.py
```

Wait for "Data ingestion complete!" message.

## Step 5: Run the Agent

```bash
python main.py
```

## Try These Queries

```
What are the top 5 rated movies?
Show me Christopher Nolan movies
Find action movies from the 2000s
What movies has Tom Hanks been in?
```

## Troubleshooting

**MongoDB not running?**
- Windows: `net start MongoDB`
- Check Task Manager for `mongod.exe`

**OpenAI API error?**
- Verify your API key in `.env`
- Check you have credits at platform.openai.com

**No movies found?**
- Run `python data_ingestion.py` again

---

That's it! You're ready to explore movies with AI! 🎬
