"""
Main Application - Interactive Movie AI Agent
Run this to interact with the AI agent through the command line
"""

from agent import MovieAgent
from dotenv import load_dotenv
import os

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
    print(banner)

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
    print(help_text)

def main():
    """Main application loop"""
    # Load environment variables
    load_dotenv()
    
    print_banner()
    print("\n🚀 Initializing AI Agent...")
    
    try:
        agent = MovieAgent()
        print("✅ Agent initialized successfully!\n")
    except Exception as e:
        print(f"❌ Error initializing agent: {str(e)}")
        print("\nMake sure:")
        print("1. MongoDB is running and accessible")
        print("2. You've run data_ingestion.py to load the data")
        print("3. Ollama is running (ollama serve)")
        print("4. The mistral model is available (ollama pull mistral)")
        return
    
    print_help()
    print("\n" + "="*60)
    print("💬 Start chatting with the Movie AI Agent!")
    print("="*60 + "\n")
    
    # Main interaction loop
    while True:
        try:
            # Get user input
            user_input = input("\n🎬 You: ").strip()
            
            # Handle empty input
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using Movie AI Agent! Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            # Query the agent
            print("\n🤖 Agent: ", end="", flush=True)
            response = agent.query(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'help' for examples.")
    
    # Cleanup
    agent.close()
    print("\n✅ Agent closed successfully.")

if __name__ == "__main__":
    main()
