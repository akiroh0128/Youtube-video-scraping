# YouTube Gaming Videos Data Scraper

A Python script to collect data from YouTube gaming videos using the YouTube Data API. This script allows you to gather detailed information about videos in any gaming genre, including metadata, statistics, and captions.

## Features

- Search for top gaming videos by genre
- Collect comprehensive video information including:
  - Video URL and basic metadata
  - Channel information
  - View and comment counts
  - Video duration
  - Publishing date
  - Video categories
  - Tags and topics
  - Location data (if available)
  - Captions/transcripts (when available)
- Real-time progress tracking
- Automatic CSV file generation with genre-based naming

## Prerequisites

### Python Version
- Python 3.6 or higher

### Required Packages
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas isodate youtube-transcript-api
```

### YouTube Data API Key
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy your API key for use in the script

## Installation

1. Clone the repository or download the script
2. Install the required packages
3. Replace `'YOUR_API_KEY_HERE'` in the script with your actual YouTube Data API key

## Usage

1. Basic usage with default settings:
```python
python scraper.py
```

2. To modify the genre or number of videos, edit the following lines in the `main()` function:
```python
genre = "gaming"  # Change to your desired genre
video_ids = scraper.search_videos(genre, max_results=500)  # Adjust max_results as needed
```

## Output

The script generates a CSV file named based on the genre (e.g., `gaming_videos.csv`) containing the following information for each video:
- Video URL
- Title
- Description
- Channel Title
- Keyword Tags
- YouTube Video Category
- Topic Details
- Video Published Date
- Video Duration
- View Count
- Comment Count
- Location of Recording (if available)
- Captions Available (true/false)
- Caption Text (if available)

## API Quota Considerations

- The script implements delays between API calls to respect YouTube's quota limits
- Each search operation and video details request counts toward your daily quota
- Monitor your API usage in the Google Cloud Console
- Consider implementing additional rate limiting for larger datasets

## Error Handling

The script includes error handling for common issues:
- API errors
- Missing video information
- Unavailable captions
- Invalid genre names
- Network connectivity issues

## Limitations

- Maximum of 500 videos per search
- Subject to YouTube API daily quota limits
- Caption extraction only works for videos with available captions
- Some location data may be unavailable
- API key must have proper YouTube Data API access enabled

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This script is for educational purposes and should be used in accordance with YouTube's terms of service and API policies. Be sure to comply with all applicable usage guidelines and data protection regulations.
