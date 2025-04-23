#!/usr/bin/env python3
"""
Script to run the LeetCode API

This script starts the LeetCode Crew API using uvicorn.
Utilizes a crew of specialized agents with Claude-3-7-Sonnet model.
"""
import os
import argparse
import uvicorn
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Check if we need to create a .env file from the example
if not os.path.exists(".env") and os.path.exists(".env.example"):
    print("⚠️  No .env file found but .env exists")
    print("   Consider creating a .env file: cp .env .env")
    print("   Then add your ANTHROPIC_API_KEY to the .env file")

def main():
    """Run the LeetCode Agent API application"""
    parser = argparse.ArgumentParser(description="Run the LeetCode Agent API server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the server to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    
    # Determine which model provider to use
    model_provider = os.environ.get("MODEL_PROVIDER", "openai").lower()
    
    # Check if proper API key is available based on model provider
    if model_provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("❌ ERROR: OPENAI_API_KEY environment variable is not set or has default value")
            print("The LeetCode crew cannot function without an API key. Please set it in your .env file:")
            print("1. Create a .env file in the project root if it doesn't exist")
            print("2. Add OPENAI_API_KEY=your_key_here to the .env file")
            return
    elif model_provider == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("❌ ERROR: ANTHROPIC_API_KEY environment variable is not set")
            print("The LeetCode crew cannot function without an API key. Please set it in your .env file:")
            print("1. Create a .env file in the project root if it doesn't exist")
            print("2. Add ANTHROPIC_API_KEY=your_key_here to the .env file")
            return
    else:
        print(f"❌ ERROR: Unsupported model provider: {model_provider}")
        print("Please set MODEL_PROVIDER to 'openai' or 'anthropic' in your .env file")
        return
    
    print(f"🤖 Starting LeetCode Crew API server at http://{args.host}:{args.port}")
    print(f"📚 API documentation will be available at http://localhost:{args.port}/docs")
    print(f"🔑 Using API key found in environment variables")
    
    # Display the correct model information based on the provider
    if model_provider == "openai":
        print(f"🧠 Using OpenAI's o3-mini-2025-01-31 model for solution generation")
    else:
        print(f"🧠 Using Claude-3-7-Sonnet model for solution generation")
        
    print(f"👥 Crew of agents: LeetCode Expert, Helper Assistant")
    print(f"🌐 Endpoint: http://localhost:{args.port}/api/leetcode-solutions")
    
    # Run the server with crew-based implementation
    uvicorn.run(
        "src.crew_api:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
