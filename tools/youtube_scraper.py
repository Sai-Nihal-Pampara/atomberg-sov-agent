import os
import json
from typing import List, Dict, Any
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

class YouTubeScraper:
    def __init__(self):
        self.api_key = config.YOUTUBE_API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        
    def search_videos(self, query: str = None, max_results: int = None) -> List[Dict]:
        """Search for videos on YouTube"""
        if query is None:
            query = config.SEARCH_QUERY
        if max_results is None:
            max_results = config.TOP_N_RESULTS
            
        try:
            # Search for videos
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                type='video',
                order='relevance'
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_id = item['id']['videoId']
                video_info = {
                    'video_id': video_id,
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnails': item['snippet']['thumbnails']
                }
                
                # Get video statistics
                stats = self.get_video_stats(video_id)
                video_info.update(stats)
                
                # Get comments
                comments = self.get_video_comments(video_id)
                video_info['comments'] = comments
                
                videos.append(video_info)
                
            return videos
            
        except HttpError as e:
            print(f"An error occurred: {e}")
            return []
    
    def get_video_stats(self, video_id: str) -> Dict:
        """Get video statistics"""
        try:
            stats_response = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()
            
            if stats_response['items']:
                stats = stats_response['items'][0]['statistics']
                return {
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0))
                }
        except HttpError as e:
            print(f"Error getting stats for video {video_id}: {e}")
        
        return {'view_count': 0, 'like_count': 0, 'comment_count': 0}
    
    def get_video_comments(self, video_id: str, max_comments: int = 100) -> List[Dict]:
        """Get comments for a video"""
        comments = []
        try:
            comments_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_comments,
                order='relevance'
            ).execute()
            
            for item in comments_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt']
                })
                
        except HttpError as e:
            print(f"Error getting comments for video {video_id}: {e}")
        
        return comments

def search_youtube_videos():
    """Main function to search YouTube videos"""
    scraper = YouTubeScraper()
    return scraper.search_videos()

if __name__ == "__main__":
    videos = search_youtube_videos()
    print(f"Found {len(videos)} videos")
    for video in videos[:3]:  # Show first 3 videos
        print(f"Title: {video['title']}")
        print(f"Views: {video['view_count']}")
        print(f"Comments: {len(video['comments'])}")
        print("---")
