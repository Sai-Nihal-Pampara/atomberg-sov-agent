#!/usr/bin/env python3
"""
Atomberg Share of Voice Analysis - Main Application
Clean, working version with both simple and CrewAI analysis
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from quick_analysis import main as run_simple_analysis
import config

def check_ollama_available():
    """Check if Ollama is available and running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def run_crewai_analysis():
    """Run CrewAI analysis if available"""
    try:
        from agents.sov_agent import main as run_crewai
        return run_crewai()
    except ImportError as e:
        print(f"❌ CrewAI not available: {e}")
        print("   Install with: pip install crewai langchain langchain-community")
        return None
    except Exception as e:
        print(f"❌ CrewAI analysis failed: {e}")
        return None

def main():
    """Main application entry point"""
    print("🎯 Atomberg Share of Voice Analysis")
    print("=" * 50)
    print(f"Search Query: {config.SEARCH_QUERY}")
    print(f"Target Brand: {config.TARGET_BRAND}")
    print(f"Competitors: {', '.join(config.COMPETITOR_BRANDS)}")
    print(f"Top N Results: {config.TOP_N_RESULTS}")
    print("=" * 50)
    
    # Check if CrewAI and Ollama are available
    try:
        import crewai
        print("\n🤖 CrewAI detected...")
        
        # Check if Ollama is running
        if check_ollama_available():
            print("✅ Ollama detected - Running CrewAI analysis...")
            result = run_crewai_analysis()
            
            if result:
                print("\n📈 CrewAI Analysis Summary:")
                print(f"   • Analysis completed successfully with AI agents")
                print(f"   • Report generated with strategic insights")
                print(f"   • Check 'crewai_analysis_report.md' for full results")
            else:
                print("\n⚠️  CrewAI analysis failed - Running simple analysis...")
                run_simple_analysis()
        else:
            print("\n⚠️  Ollama not detected - Running simple analysis...")
            print("   To use CrewAI with Ollama:")
            print("   1. Install Ollama: https://ollama.ai/download")
            print("   2. Start Ollama service")
            print("   3. Run this script again")
            run_simple_analysis()
        
    except ImportError:
        print("\n⚠️  CrewAI not available - Running simple analysis...")
        print("   Install CrewAI with: pip install crewai langchain langchain-community")
        run_simple_analysis()

if __name__ == "__main__":
    main()
