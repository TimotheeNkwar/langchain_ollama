"""
Main Application - Interactive Movie AI Agent
Run this to interact with the AI agent through the command line
"""

from agent import MovieAgent
from dotenv import load_dotenv
from loguru import logger
import sys

# Configure loguru for main.py
logger.remove()  # Remove default handler
logger.add(
    "main.log",
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    backtrace=True,
    diagnose=True,
    encoding="utf-8"
)
logger.add(
    sys.stdout,
    level="INFO",
    format="{message}",
    colorize=True
)

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          🎬 IMDB Movie AI Agent with LangChain 🎬        ║
    ║                                                           ║
    ║       Powered by MongoDB, LangChain, and Ollama          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    logger.info(banner)

def print_help():
    """Print help information"""
    help_text = """
    📚 Example Questions You Can Ask:
    
    🎯 Search & Discovery:
    - "What are the top 10 rated movies?"
    - "Find movies about space or sci-fi"
    - "Show me Christopher Nolan movies"
    - "What are the best drama movies?"
    
    🎭 Actor & Director Queries:
    - "What movies has Leonardo DiCaprio been in?"
    - "Show me all Quentin Tarantino films"
    - "Find movies with Tom Hanks"
    
    📅 Time-based Queries:
    - "What are the best movies from the 1990s?"
    - "Show me movies between 2000 and 2010"
    - "Find recent action movies"
    
    📊 Statistics & Analysis:
    - "What are the database statistics?"
    - "Who are the most prolific directors?"
    - "What's the average rating of movies?"
    
    💡 Recommendations:
    - "Recommend a thriller movie"
    - "I want to watch something like Inception"
    - "Suggest a classic movie"
    
    Commands:
    - 'help' - Show this help message
    - 'exit' or 'quit' - Exit the application
    """
    logger.info(help_text)

def main():
    """Main application loop"""
    # Load environment variables
    load_dotenv()

    print_banner()
    logger.info("\n🚀 Initializing AI Agent...")

    agent = None
    try:
        agent = MovieAgent()
        logger.info("✅ Agent initialized successfully!\n")
    except Exception as e:
        logger.error(f"❌ Error initializing agent: {str(e)}")
        logger.info("\nMake sure:")
        logger.info("1. MongoDB is running and accessible")
        logger.info("2. You've run data_ingestion.py to load the data")
        logger.info("3. Ollama is running (ollama serve)")
        logger.info("4. The mistral model is available (ollama pull mistral)")
        return 1

    print_help()
    logger.info("\n" + "="*60)
    logger.info("💬 Start chatting with the Movie AI Agent!")
    logger.info("="*60 + "\n")

    # Main interaction loop
    try:
        while True:
            try:
                # Get user input
                user_input = input("\n🎬 You: ").strip()

                # Handle empty input
                if not user_input:
                    continue

                # Handle commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    logger.info("\n👋 Thank you for using Movie AI Agent! Goodbye!")
                    break

                if user_input.lower() == 'help':
                    print_help()
                    continue

                # Query the agent
                logger.info("\n🤖 Agent: ")
                response = agent.query(user_input)
                logger.info(response)

            except KeyboardInterrupt:
                logger.info("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                logger.error(f"\n❌ Error: {str(e)}")
                logger.info("Please try again or type 'help' for examples.")
    finally:
        # Cleanup
        if agent:
            agent.close()
            logger.info("\n✅ Agent closed successfully.")

    return 0

if __name__ == "__main__":
    main()
