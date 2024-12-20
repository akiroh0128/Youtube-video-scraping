import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
import pandas as pd
import json
import isodate
from datetime import datetime
import time
from youtube_transcript_api import YouTubeTranscriptApi

class YouTubeDataScraper:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.videos_data = []
        self.genre = None
        self.category_mapping = self._fetch_video_categories()
        
    def _fetch_video_categories(self):
        print("\nFetching YouTube video category mappings...")
        category_mapping = {}
        try:
            request = self.youtube.videoCategories().list(
                part='snippet',
                regionCode='US'  # Adjust region code if needed
            )
            response = request.execute()
            for item in response['items']:
                category_id = item['id']
                category_name = item['snippet']['title']
                category_mapping[category_id] = category_name
            print("Video category mappings fetched successfully.")
        except HttpError as e:
            print(f"An HTTP error occurred while fetching categories: {e}")
        return category_mapping
        
    def _get_safe_filename(self, genre):
        return genre.lower().replace(' ', '_').replace('&', 'and').replace('/', '_')
    
    def search_videos(self, genre, max_results=500):
        self.genre = genre  
        videos = []
        next_page_token = None
        
        print(f"\nSearching for {max_results} videos in the '{genre}' genre...")
        
        while len(videos) < max_results:
            try:
                search_request = self.youtube.search().list(
                    part='id',
                    q=genre,
                    type='video',  
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token,
                    order='viewCount'  # Get popular videos first
                )
                search_response = search_request.execute()
                
                # Extract video IDs
                video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
                videos.extend(video_ids)
                
                # Print progress
                print(f"Found {len(videos)}/{max_results} videos...", end='\r')
                
                next_page_token = search_response.get('nextPageToken')
                if not next_page_token:
                    break
                    
                time.sleep(0.5)
                
            except HttpError as e:
                print(f"\nAn HTTP error occurred: {e}")
                break
        
        print(f"\nCompleted video search. Found {len(videos)} videos.")
        return videos[:max_results]
    
    def get_video_details(self, video_ids):
        total_videos = len(video_ids)
        processed_videos = 0
        
        print("\nCollecting detailed information for each video...")
        
        for i in range(0, total_videos, 50):  # Process in batches of 50
            batch = video_ids[i:i + 50]
            try:
                videos_request = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics,recordingDetails,topicDetails',
                    id=','.join(batch)
                )
                videos_response = videos_request.execute()
                
                for video in videos_response['items']:
                    category_id = video['snippet']['categoryId']
                    category_name = self.category_mapping.get(category_id, "Unknown Category")
                    video_data = {
                        'Video URL': f"https://www.youtube.com/watch?v={video['id']}",
                        'Title': video['snippet']['title'],
                        'Description': video['snippet']['description'],
                        'Channel Title': video['snippet']['channelTitle'],
                        'Keyword Tags': ','.join(video['snippet'].get('tags', [])),
                        'YouTube Video Category': category_name,
                        'Topic Details': ','.join(video.get('topicDetails', {}).get('topicCategories', [])),
                        'Video Published at': video['snippet']['publishedAt'],
                        'Video Duration': str(isodate.parse_duration(video['contentDetails']['duration'])),
                        'View Count': video['statistics'].get('viewCount', 0),
                        'Comment Count': video['statistics'].get('commentCount', 0),
                        'Location of Recording': self._get_location(video.get('recordingDetails', {}))
                    }
                    
                    # Check and get captions
                    try:
                        transcript = YouTubeTranscriptApi.get_transcript(video['id'])
                        video_data['Captions Available'] = True
                        video_data['Caption Text'] = ' '.join([entry['text'] for entry in transcript])
                    except:
                        video_data['Captions Available'] = False
                        video_data['Caption Text'] = ''
                    
                    self.videos_data.append(video_data)
                    processed_videos += 1
                    
                    # Print progress
                    progress = (processed_videos / total_videos) * 100
                    print(f"Progress: {processed_videos}/{total_videos} videos processed ({progress:.1f}%)...", end='\r')
                
                time.sleep(0.5)
                
            except HttpError as e:
                print(f"\nAn HTTP error occurred: {e}")
                continue
        
        print(f"\nCompleted collecting detailed information for {processed_videos} videos.")
    
    def _get_location(self, recording_details):
        if not recording_details:
            return ''
        
        location_parts = []
        if 'locationDescription' in recording_details:
            location_parts.append(recording_details['locationDescription'])
        if 'location' in recording_details:
            loc = recording_details['location']
            if 'latitude' in loc and 'longitude' in loc:
                location_parts.append(f"{loc['latitude']}, {loc['longitude']}")
        
        return ' - '.join(location_parts)
    
    def save_to_csv(self):
        if not self.genre:
            raise ValueError("Genre not set. Please run search_videos() first.")
        
        filename = f'{self.genre}_videos_data.csv'
        df = pd.DataFrame(self.videos_data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nData saved to {filename} ({len(self.videos_data)} records)")

def main():
    # Replace with your API key
    API_KEY = 'YOUR_API_KEY_HERE'
    
    scraper = YouTubeDataScraper(API_KEY)
    
    start_time = time.time()
    
    genre = "gaming"  # You can change this to any genre
    
    video_ids = scraper.search_videos(genre, max_results=500)
    
    scraper.get_video_details(video_ids)
    
    scraper.save_to_csv()
    
    end_time = time.time()
    runtime = end_time - start_time
    print(f"\nTotal runtime: {runtime:.2f} seconds ({runtime/60:.2f} minutes)")
    print("Data collection complete!")

if __name__ == "__main__":
    main()
