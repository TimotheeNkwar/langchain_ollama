"""
Quick launcher for the FastAPI server
Alternative to running: uvicorn api:app --reload
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
os.environ['API_HOST'] = os.getenv('API_HOST', '0.0.0.0')
os.environ['API_PORT'] = os.getenv('API_PORT', '8000')
os.environ['API_DEBUG'] = os.getenv('API_DEBUG', 'True')
if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', 8000)),
        reload=os.getenv('API_DEBUG', 'True') == 'True',
        log_level=os.getenv('LOG_LEVEL', 'info')
    )
