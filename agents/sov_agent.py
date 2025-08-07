#!/usr/bin/env python3
"""
CrewAI Agents for Atomberg Share of Voice Analysis
Clean, working implementation with LangChain and CrewAI
"""

from crewai import Agent, Task, Crew, Process
from langchain_ollama import OllamaLLM
from typing import List, Dict, Any
import json
from datetime import datetime

from tools.youtube_scraper import search_youtube_videos
import config

class SoVAnalysisAgent:
    """CrewAI-based Share of Voice Analysis Agent"""
    
    def __init__(self):
        # Initialize Ollama LLM with correct format for CrewAI
        self.llm = OllamaLLM(
            base_url=config.OLLAMA_BASE_URL,
            model="ollama/gemma3:1b",  # Use the full model name format
            temperature=0.7
        )
        
    def _analyze_sov_simple(self, videos):
        """Simple Share of Voice analysis"""
        brands = [config.TARGET_BRAND] + config.COMPETITOR_BRANDS
        total_mentions = {brand: 0 for brand in brands}
        positive_mentions = {brand: 0 for brand in brands}
        negative_mentions = {brand: 0 for brand in brands}
        
        total_comments = 0
        
        for video in videos:
            comments = video.get('comments', [])
            total_comments += len(comments)
            
            for comment in comments:
                comment_text = comment.get('text', '').lower()
                
                # Check for brand mentions
                for brand in brands:
                    if brand in comment_text:
                        total_mentions[brand] += 1
                        
                        # Simple sentiment analysis
                        sentiment = self._simple_sentiment_analysis(comment_text)
                        if sentiment == 'positive':
                            positive_mentions[brand] += 1
                        elif sentiment == 'negative':
                            negative_mentions[brand] += 1
        
        # Calculate percentages
        total_all_mentions = sum(total_mentions.values())
        sov_percentages = {}
        positive_sov = {}
        
        for brand in brands:
            if total_all_mentions > 0:
                sov_percentages[brand] = (total_mentions[brand] / total_all_mentions) * 100
            else:
                sov_percentages[brand] = 0
                
            total_positive = sum(positive_mentions.values())
            if total_positive > 0:
                positive_sov[brand] = (positive_mentions[brand] / total_positive) * 100
            else:
                positive_sov[brand] = 0
        
        return {
            'total_mentions': total_mentions,
            'positive_mentions': positive_mentions,
            'negative_mentions': negative_mentions,
            'sov_percentages': sov_percentages,
            'positive_sov': positive_sov,
            'total_comments': total_comments,
            'videos_analyzed': len(videos)
        }
    
    def _simple_sentiment_analysis(self, text):
        """Simple sentiment analysis"""
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'perfect', 'awesome', 'fantastic', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'disappointing', 'poor', 'horrible', 'useless', 'broken']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
        
    def create_agents(self):
        """Create specialized agents with Ollama LLM"""
        
        # Data Collection Agent
        data_collector = Agent(
            role='YouTube Data Collector',
            goal='Collect comprehensive data from YouTube search results for smart fan videos',
            backstory="""You are an expert data collector specializing in YouTube content analysis. 
            Your job is to gather detailed information about videos, comments, and engagement metrics 
            to provide a complete picture of the smart fan market on YouTube.""",
            llm=self.llm,
            verbose=True
        )
        
        # Sentiment Analysis Agent
        sentiment_analyzer = Agent(
            role='Sentiment Analysis Expert',
            goal='Analyze sentiment and Share of Voice metrics for Atomberg and competitors',
            backstory="""You are a sentiment analysis expert with deep knowledge of brand perception 
            and Share of Voice analysis. You understand how to interpret mentions, sentiment, and 
            engagement to provide actionable insights for marketing teams.""",
            llm=self.llm,
            verbose=True
        )
        
        # Insights and Recommendations Agent
        insights_agent = Agent(
            role='Marketing Insights Specialist',
            goal='Generate actionable insights and recommendations for Atomberg\'s marketing team',
            backstory="""You are a marketing strategy expert who specializes in competitive analysis 
            and brand positioning. You understand market dynamics and can provide strategic 
            recommendations based on data analysis.""",
            llm=self.llm,
            verbose=True
        )
        
        return data_collector, sentiment_analyzer, insights_agent
    
    def create_tasks(self, data_collector, sentiment_analyzer, insights_agent):
        """Create tasks for the agents"""
        
        # Task 1: Data Collection
        data_collection_task = Task(
            description="""Search YouTube for smart fan videos and collect comprehensive data including:
            1. Video metadata (title, description, views, likes)
            2. Comment data with sentiment analysis
            3. Brand mention tracking for Atomberg and competitors
            4. Engagement metrics analysis
            
            Use the collected data to understand the current market landscape.""",
            agent=data_collector,
            expected_output="Comprehensive dataset of YouTube videos and comments with brand mentions"
        )
        
        # Task 2: Sentiment Analysis
        sentiment_analysis_task = Task(
            description="""Analyze the collected data to determine:
            1. Share of Voice percentages for all brands
            2. Sentiment distribution (positive/negative/neutral)
            3. Positive Share of Voice metrics
            4. Competitive positioning analysis
            
            Provide detailed insights about Atomberg's market position.""",
            agent=sentiment_analyzer,
            expected_output="Detailed Share of Voice and sentiment analysis report"
        )
        
        # Task 3: Strategic Insights
        insights_task = Task(
            description="""Based on the analysis, generate strategic insights including:
            1. Current market position assessment
            2. Competitive advantage identification
            3. Content strategy recommendations
            4. Actionable next steps for marketing team
            
            Focus on practical recommendations that can be implemented immediately.""",
            agent=insights_agent,
            expected_output="Strategic insights and actionable recommendations"
        )
        
        return [data_collection_task, sentiment_analysis_task, insights_task]
    
    def run_analysis(self):
        """Run the complete CrewAI analysis"""
        print("🚀 Starting CrewAI-powered Share of Voice Analysis...")
        print("=" * 60)
        
        try:
            # First, collect the data
            print("📊 Collecting YouTube data...")
            videos = search_youtube_videos()
            print(f"✅ Collected data from {len(videos)} videos")
            
            # Create agents
            data_collector, sentiment_analyzer, insights_agent = self.create_agents()
            
            # Create tasks
            tasks = self.create_tasks(data_collector, sentiment_analyzer, insights_agent)
            
            # Create crew
            crew = Crew(
                agents=[data_collector, sentiment_analyzer, insights_agent],
                tasks=tasks,
                verbose=True,
                process=Process.sequential
            )
            
            # Run the analysis
            result = crew.kickoff()
            
            return result
            
        except Exception as e:
            print(f"❌ CrewAI analysis failed: {e}")
            return None
    
    def generate_report(self, result):
        """Generate a comprehensive report from CrewAI results"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
# Atomberg Share of Voice Analysis Report
**Generated on:** {timestamp}
**Analysis Method:** CrewAI with Ollama ({config.OLLAMA_MODEL})
**Search Query:** {config.SEARCH_QUERY}
**Target Brand:** {config.TARGET_BRAND}
**Competitors:** {', '.join(config.COMPETITOR_BRANDS)}

## Executive Summary

This analysis was conducted using CrewAI agents powered by Ollama for comprehensive Share of Voice analysis.

## AI Agent Analysis Results

{result}

## Key Findings

- Analysis completed using 3 specialized AI agents
- Data collection, sentiment analysis, and strategic insights generated
- Recommendations provided for marketing team

## Next Steps

1. Review the AI-generated insights
2. Implement recommended strategies
3. Monitor performance metrics
4. Conduct follow-up analysis

---
*Report generated by CrewAI + Ollama*
        """
        
        return report

def main():
    """Main function to run CrewAI analysis"""
    agent = SoVAnalysisAgent()
    result = agent.run_analysis()
    
    if result:
        # Generate and save report
        report = agent.generate_report(result)
        
        with open('crewai_analysis_report.md', 'w', encoding='utf-8') as f:
            f.write(report)
        
        print("\n" + "=" * 60)
        print("✅ CrewAI Analysis Complete!")
        print(f"📄 Report saved to: crewai_analysis_report.md")
        print("=" * 60)
        
        return result
    else:
        print("❌ Analysis failed. Check the logs for errors.")
        return None

if __name__ == "__main__":
    main()
