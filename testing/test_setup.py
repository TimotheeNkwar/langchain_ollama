"""
Setup Verification Script
Run this to check if your environment is properly configured
"""

import sys
from dotenv import load_dotenv
import os

def print_status(check_name, status, message=""):
    """Print formatted status message"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {check_name}: {message}")
    return status

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 8
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    return print_status(
        "Python Version",
        is_valid,
        f"{version_str} {'(OK)' if is_valid else '(Need 3.8+)'}"
    )

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'langchain',
        'langchain_community',
        'langchain_ollama',
        'pymongo',
        'pandas',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'dotenv':
                __import__('dotenv')
            else:
                __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print_status(
            "Dependencies",
            False,
            f"Missing: {', '.join(missing)}"
        )
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        return print_status("Dependencies", True, "All packages installed")

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print_status(".env File", False, "File not found")
        print("   Run: copy .env.example .env")
        return False
    
    load_dotenv()
    
    ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    ollama_model = os.getenv('OLLAMA_MODEL', 'mistral')
    mongodb_uri = os.getenv('MONGODB_URI')
    
    print_status("Ollama Base URL", True, ollama_url)
    print_status("Ollama Model", True, ollama_model)
    print_status("MongoDB URI", True, mongodb_uri or "Using default")
    return True

def check_mongodb():
    """Check MongoDB connection"""
    try:
        from pymongo import MongoClient
        from pymongo.errors import ServerSelectionTimeoutError
        
        load_dotenv()
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=3000)
        client.server_info()  # Force connection
        
        print_status("MongoDB Connection", True, "Connected successfully")
        client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print_status("MongoDB Connection", False, "Cannot connect")
        print("   Make sure MongoDB is running")
        print("   Windows: net start MongoDB")
        return False
    except Exception as e:
        print_status("MongoDB Connection", False, str(e))
        return False

def check_ollama():
    """Check if Ollama is running and model is available"""
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            load_dotenv()
            model = os.getenv('OLLAMA_MODEL', 'mistral')
            if model in result.stdout:
                print_status("Ollama Service", True, f"Running with {model} model")
                return True
            else:
                print_status("Ollama Service", False, f"Model '{model}' not found")
                print(f"   Run: ollama pull {model}")
                return False
        else:
            print_status("Ollama Service", False, "Not running")
            print("   Start Ollama or run: ollama pull mistral")
            return False
    except FileNotFoundError:
        print_status("Ollama Service", False, "Ollama not installed")
        print("   Install from: https://ollama.ai/")
        return False
    except Exception as e:
        print_status("Ollama Service", False, f"Error: {str(e)}")
        return False

def check_data():
    """Check if data is loaded in MongoDB"""
    try:
        from pymongo import MongoClient
        
        load_dotenv()
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('MONGODB_DATABASE')
        collection_name = os.getenv('MONGODB_COLLECTION')
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=3000)
        db = client[database_name]
        collection = db[collection_name]
        
        count = collection.count_documents({})
        client.close()
        
        if count == 0:
            print_status("Data Loaded", False, "No movies in database")
            print("   Run: python data_ingestion.py")
            return False
        elif count < 10000:
            print_status("Data Loaded", True, f"{count:,} movies in database (partial load)")
            return True
        else:
            print_status("Data Loaded", True, f"{count:,} movies in database")
            return True
            
    except Exception as e:
        print_status("Data Loaded", False, "Cannot check (MongoDB not connected)")
        return False

def check_csv_file():
    """Check if CSV file exists"""
    if os.path.exists('dataset/TMDB_movie_dataset_v11.csv'):
        return print_status("CSV File", True, "TMDB dataset found (50,000 movies)")
    elif os.path.exists('dataset/TMDB_movie_dataset_5k.csv'):
        return print_status("CSV File", True, "TMDB subset found (5,000 movies)")
    elif os.path.exists('dataset/movies.csv'):
        return print_status("CSV File", True, "Legacy IMDB dataset found (deprecated)")
    else:
        return print_status("CSV File", False, "TMDB_movie_dataset_v11.csv not found in dataset/")

def main():
    """Run all checks"""
    print("="*60)
    print("🔍 TMDB Movie AI Agent - Setup Verification")
    print("="*60)
    print()
    
    checks = []
    
    # Run all checks
    checks.append(check_python_version())
    checks.append(check_dependencies())
    checks.append(check_csv_file())
    checks.append(check_env_file())
    checks.append(check_ollama())
    checks.append(check_mongodb())
    checks.append(check_data())
    
    print()
    print("="*60)
    
    if all(checks):
        print("✅ All checks passed! You're ready to run the agent.")
        print()
        print("Start the agent with: python main.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Quick fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install Ollama: https://ollama.ai/")
        print("3. Pull a model: ollama pull mistral")
        print("4. Configure .env: copy .env.example .env (then edit)")
        print("5. Start MongoDB: net start MongoDB")
        print("6. Load data: python data_ingestion.py")
    
    print("="*60)

if __name__ == "__main__":
    main()
