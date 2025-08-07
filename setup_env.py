#!/usr/bin/env python3
"""
Environment Setup Script for Atomberg SoV Analysis
Helps users configure their .env file with required settings
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with default values"""
    env_content = """# YouTube API Configuration
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY_HERE

# Ollama Configuration (for CrewAI)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma3:1b

# Analysis Configuration
SEARCH_QUERY=smart fan
TOP_N_RESULTS=50
TARGET_BRAND=atomberg
COMPETITOR_BRANDS=crompton,havells,orient,usha,bajaj
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with default values")

def check_env_file():
    """Check if .env file exists and has required values"""
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file found")
    
    # Load and check values
    from dotenv import load_dotenv
    load_dotenv()
    
    youtube_key = os.getenv("YOUTUBE_API_KEY")
    if youtube_key == "YOUR_YOUTUBE_API_KEY_HERE" or not youtube_key:
        print("⚠️  YouTube API key not set")
        print("   Please update YOUTUBE_API_KEY in .env file")
        return False
    else:
        print("✅ YouTube API key is set")
    
    return True

def get_youtube_api_instructions():
    """Print instructions for getting YouTube API key"""
    print("\n📋 How to Get YouTube API Key:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Enable YouTube Data API v3")
    print("4. Create credentials (API Key)")
    print("5. Copy the API key")
    print("6. Update YOUTUBE_API_KEY in .env file")

def main():
    """Main setup function"""
    print("🔧 Environment Setup for Atomberg SoV Analysis")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        create_env_file()
    
    # Check current configuration
    if check_env_file():
        print("\n🎉 Environment is properly configured!")
        print("You can now run the analysis with:")
        print("   python simple_analysis.py")
    else:
        print("\n❌ Environment needs configuration")
        get_youtube_api_instructions()
        print("\nAfter setting the API key, run:")
        print("   python setup_env.py")

if __name__ == "__main__":
    main()
