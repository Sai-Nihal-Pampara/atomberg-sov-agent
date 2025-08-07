#!/usr/bin/env python3
"""
Quick Atomberg Share of Voice Analysis
Simplified version without heavy dependencies
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from tools.youtube_scraper import search_youtube_videos
import config

def simple_sentiment_analysis(text):
    """Simple sentiment analysis without heavy dependencies"""
    text_lower = text.lower()
    
    # Simple positive/negative word lists
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

def analyze_sov_simple(videos):
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
                    sentiment = simple_sentiment_analysis(comment_text)
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

def main():
    """Main analysis function"""
    print("🎯 Quick Atomberg Share of Voice Analysis")
    print("=" * 50)
    print(f"Search Query: {config.SEARCH_QUERY}")
    print(f"Target Brand: {config.TARGET_BRAND}")
    print(f"Competitors: {', '.join(config.COMPETITOR_BRANDS)}")
    print(f"Top N Results: {config.TOP_N_RESULTS}")
    print("=" * 50)
    
    try:
        # Search for videos
        print("\n🔍 Searching YouTube for smart fan videos...")
        videos = search_youtube_videos()
        
        if not videos:
            print("❌ No videos found. Please check your search query and API key.")
            return
        
        print(f"✅ Found {len(videos)} videos")
        
        # Analyze Share of Voice
        print("\n🧠 Analyzing Share of Voice...")
        results = analyze_sov_simple(videos)
        
        # Display results
        print("\n📊 Share of Voice Results:")
        print("-" * 40)
        
        for brand in [config.TARGET_BRAND] + config.COMPETITOR_BRANDS:
            mentions = results['total_mentions'][brand]
            sov = results['sov_percentages'][brand]
            positive_sov = results['positive_sov'][brand]
            
            print(f"• {brand.title()}: {sov:.1f}% ({mentions} mentions)")
            print(f"  - Positive SoV: {positive_sov:.1f}%")
        
        print(f"\n📈 Summary:")
        print(f"• Total videos analyzed: {results['videos_analyzed']}")
        print(f"• Total comments analyzed: {results['total_comments']}")
        print(f"• Total brand mentions: {sum(results['total_mentions'].values())}")
        
        # Generate insights
        atomberg_sov = results['sov_percentages'][config.TARGET_BRAND]
        competitors = {k: v for k, v in results['sov_percentages'].items() if k != config.TARGET_BRAND}
        top_competitor = max(competitors, key=competitors.get) if competitors else None
        
        print(f"\n💡 Key Insights:")
        print(f"• {config.TARGET_BRAND.title()} has {atomberg_sov:.1f}% Share of Voice")
        if top_competitor:
            competitor_sov = results['sov_percentages'][top_competitor]
            print(f"• Top competitor: {top_competitor.title()} ({competitor_sov:.1f}%)")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"quick_analysis_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n✅ Analysis complete! Results saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Please check your YouTube API key in the .env file")

if __name__ == "__main__":
    main()
