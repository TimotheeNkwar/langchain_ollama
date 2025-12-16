"""
Data Ingestion Script for IMDB Top 1000 Movies
Loads CSV data into MongoDB with proper data cleaning and structuring
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

    # Read CSV
    print("Reading CSV file...")
    df = pd.read_csv('dataset/movies.csv')

    print(f"Loaded {len(df)} movies from CSV")

    # Clean and transform data
    movies = []
    for idx, row in df.iterrows():
        # Parse stars from tuple string format
        stars_list = []
        if pd.notna(row['stars']):
            try:
                # Clean up the stars string and extract names
                stars_str = str(row['stars']).replace("(", "").replace(")", "").replace("'", "")
                stars_list = [s.strip() for s in stars_str.split(',') if s.strip()]
            except:
                stars_list = []
        
        movie = {
            'poster_link': row['poster'] if pd.notna(row['poster']) else None,
            'title': row['title'] if pd.notna(row['title']) else None,
            'year': extract_year_from_title(row['title']),
            'certificate': row['certificate'] if pd.notna(row['certificate']) else None,
            'runtime_minutes': clean_runtime(row['runtime']),
            'genre': row['genre'] if pd.notna(row['genre']) else None,
            'imdb_rating': float(row['rating']) if pd.notna(row['rating']) else None,
            'overview': row['about'] if pd.notna(row['about']) else None,
            'director': row['director'] if pd.notna(row['director']) else None,
            'stars': stars_list,
            'votes': clean_numeric(row['votes']),
            'gross': row['gross_earn'] if pd.notna(row['gross_earn']) else None,
            # Create a searchable text field combining key information
            'searchable_text': f"{row['title']} {row['genre']} {row['director']} {row['about']}" if pd.notna(row['about']) else f"{row['title']} {row['genre']} {row['director']}"
        }

        movies.append(movie)

    # Insert into MongoDB
    print(f"Inserting {len(movies)} movies into MongoDB...")
    result = collection.insert_many(movies)
    print(f"Successfully inserted {len(result.inserted_ids)} movies")

    # Create indexes for better query performance
    print("Creating indexes...")
    collection.create_index('title')
    collection.create_index('year')
    collection.create_index('imdb_rating')
    collection.create_index('director')
    collection.create_index('genre')

    print("Data ingestion complete!")

    # Print some statistics
    print("\n=== Database Statistics ===")
    print(f"Total movies: {collection.count_documents({})}")
    avg_result = list(collection.aggregate([{'$group': {'_id': None, 'avg_rating': {'$avg': '$imdb_rating'}}}]))
    if avg_result:
        print(f"Average IMDB rating: {avg_result[0]['avg_rating']:.2f}")
    
    earliest = collection.find_one({'year': {'$ne': None}}, sort=[('year', 1)])
    latest = collection.find_one({'year': {'$ne': None}}, sort=[('year', -1)])
    if earliest and latest:
        print(f"Year range: {earliest['year']} - {latest['year']}")

    client.close()

if __name__ == "__main__":
    load_data_to_mongodb()
