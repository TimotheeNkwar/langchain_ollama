"""
Data Ingestion Script for TMDB Movie Dataset
Loads TMDB CSV data into MongoDB with proper data cleaning and structuring
"""

import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

def clean_numeric(value):
    """Clean numeric values by removing commas and converting to appropriate type"""
    if pd.isna(value):
        return None
    if isinstance(value, str):
        # Remove commas and quotes
        value = value.replace(',', '').replace('"', '')
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return None
    return value

def clean_runtime(runtime):
    """Extract numeric runtime in minutes"""
    if pd.isna(runtime):
        return None
    if isinstance(runtime, str):
        match = re.search(r'(\d+)', runtime)
        if match:
            return int(match.group(1))
    return None

def extract_year_from_title(title):
    """Extract year from title string if present (e.g., 'Movie Title (2010)')"""
    if pd.isna(title):
        return None
    match = re.search(r'\((\d{4})\)', str(title))
    if match:
        return int(match.group(1))
    return None

def load_data_to_mongodb():
    """Load IMDB dataset into MongoDB"""

    # MongoDB connection
    mongodb_uri = os.getenv('MONGODB_URI', )
    database_name = os.getenv('MONGODB_DATABASE')
    collection_name = os.getenv('MONGODB_COLLECTION')

    print(f"Connecting to MongoDB at {mongodb_uri}")
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    # Clear existing data
    print(f"Clearing existing data in {database_name}.{collection_name}")
    collection.delete_many({})

    # Read CSV (limit to 50,000 movies)
    print("Reading CSV file...")
    df = pd.read_csv('dataset/TMDB_movie_dataset_v11.csv', nrows=50000)

    print(f"Loaded {len(df)} movies from CSV")

    # Clean and transform data
    movies = []
    for idx, row in df.iterrows():
        # Parse year from release_date
        year = None
        if pd.notna(row['release_date']):
            try:
                year = int(str(row['release_date']).split('-')[0])
            except:
                year = None
        
        movie = {
            'tmdb_id': int(row['id']) if pd.notna(row['id']) else None,
            'imdb_id': row['imdb_id'] if pd.notna(row['imdb_id']) else None,
            'title': row['title'] if pd.notna(row['title']) else None,
            'original_title': row['original_title'] if pd.notna(row['original_title']) else None,
            'year': year,
            'release_date': row['release_date'] if pd.notna(row['release_date']) else None,
            'runtime_minutes': int(row['runtime']) if pd.notna(row['runtime']) and str(row['runtime']).replace('.','').isdigit() else None,
            'genres': row['genres'] if pd.notna(row['genres']) else None,
            'vote_average': float(row['vote_average']) if pd.notna(row['vote_average']) else None,
            'vote_count': int(row['vote_count']) if pd.notna(row['vote_count']) and str(row['vote_count']).replace('.','').isdigit() else None,
            'overview': row['overview'] if pd.notna(row['overview']) else None,
            'tagline': row['tagline'] if pd.notna(row['tagline']) else None,
            'poster_path': row['poster_path'] if pd.notna(row['poster_path']) else None,
            'backdrop_path': row['backdrop_path'] if pd.notna(row['backdrop_path']) else None,
            'popularity': float(row['popularity']) if pd.notna(row['popularity']) else None,
            'budget': int(row['budget']) if pd.notna(row['budget']) and str(row['budget']).replace('.','').isdigit() else None,
            'revenue': int(row['revenue']) if pd.notna(row['revenue']) and str(row['revenue']).replace('.','').isdigit() else None,
            'status': row['status'] if pd.notna(row['status']) else None,
            'original_language': row['original_language'] if pd.notna(row['original_language']) else None,
            'production_companies': row['production_companies'] if pd.notna(row['production_companies']) else None,
            'production_countries': row['production_countries'] if pd.notna(row['production_countries']) else None,
            'spoken_languages': row['spoken_languages'] if pd.notna(row['spoken_languages']) else None,
            'keywords': row['keywords'] if pd.notna(row['keywords']) else None,
            'homepage': row['homepage'] if pd.notna(row['homepage']) else None,
            'adult': row['adult'] == 'True' if pd.notna(row['adult']) else False,
            # Create a searchable text field combining key information
            'searchable_text': f"{row['title']} {row['genres']} {row['overview']} {row['keywords']}" if pd.notna(row['overview']) else f"{row['title']} {row['genres']}"
        }

        movies.append(movie)

    # Insert into MongoDB in batches
    print(f"Inserting {len(movies)} movies into MongoDB in batches...")
    batch_size = 1000
    total_inserted = 0
    
    for i in range(0, len(movies), batch_size):
        batch = movies[i:i + batch_size]
        try:
            result = collection.insert_many(batch, ordered=False)
            total_inserted += len(result.inserted_ids)
            print(f"Progress: {total_inserted}/{len(movies)} movies inserted ({(total_inserted/len(movies)*100):.1f}%)")
        except Exception as e:
            print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
            continue
    
    print(f"Successfully inserted {total_inserted} movies")

    # Create indexes for better query performance
    print("Creating indexes...")
    collection.create_index('title')
    collection.create_index('year')
    collection.create_index('vote_average')
    collection.create_index('tmdb_id')
    collection.create_index('imdb_id')
    collection.create_index('genres')

    print("Data ingestion complete!")

    # Print some statistics
    print("\n=== Database Statistics ===")
    print(f"Total movies: {collection.count_documents({})}")
    avg_result = list(collection.aggregate([{'$group': {'_id': None, 'avg_rating': {'$avg': '$vote_average'}}}]))
    if avg_result:
        print(f"Average TMDB rating: {avg_result[0]['avg_rating']:.2f}")
    
    earliest = collection.find_one({'year': {'$ne': None}}, sort=[('year', 1)])
    latest = collection.find_one({'year': {'$ne': None}}, sort=[('year', -1)])
    if earliest and latest:
        print(f"Year range: {earliest['year']} - {latest['year']}")

    client.close()

if __name__ == "__main__":
    load_data_to_mongodb()
