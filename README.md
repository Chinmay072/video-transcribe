# Media Insights Analyzer and Video Transcription API

This repository contains two separate applications:

1. Media Insights Analyzer: A Python application that analyzes media insights to find related YouTube videos and blog posts based on provided business intelligence and market positioning data.
2. Video Transcription API: A Flask-based API that transcribes video and audio files using AssemblyAI.

## Media Insights Analyzer

### Features

- Generates relevant search keywords from media insights
- Finds related YouTube videos using YouTube Data API
- Discovers related blog posts using News API
- Handles multiple types of media insights including demographics, pain points, and market positioning

### Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Get API Keys:
   - YouTube Data API key from [Google Cloud Console](https://console.cloud.google.com/)
   - News API key from [News API](https://newsapi.org/)

3. Update the API keys in `media_insights_analyzer.py`:
```python
youtube_api_key = "YOUR_YOUTUBE_API_KEY"
news_api_key = "YOUR_NEWS_API_KEY"
```

### Usage

```python
from media_insights_analyzer import MediaInsightsAnalyzer

# Initialize with your API keys
analyzer = MediaInsightsAnalyzer(youtube_api_key, news_api_key)

# Define your media insights
media_insights = {
    "primaryAudienceDemographics": "Your target audience",
    "painPointsAddressed": ["Pain point 1", "Pain point 2"],
    "competitors": ["Competitor 1", "Competitor 2"],
    "marketPosition": "Your market position"
}

# Generate keywords and find related content
keywords = analyzer.generate_search_keywords(media_insights)
videos = analyzer.find_related_videos(keywords)
blogs = analyzer.find_related_blogs(keywords)
```

## Video Transcription API

### Features

- Transcribe video and audio files (supports mp3, wav, mp4, m4a, webm)
- Sentence-level transcription with timestamps
- Easy-to-use REST API
- Built with Flask and AssemblyAI

### Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. The API key is already configured in the code.

### API Endpoints

#### Health Check
```bash
GET /health
```
Returns the health status of the API.

#### Transcribe Audio/Video
```bash
POST /transcribe
```
Upload a video or audio file for transcription.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (audio/video file)

**Response:**
```json
{
    "success": true,
    "sentences": [
        {
            "text": "This is the first sentence.",
            "start_time": 0.0,
            "end_time": 2.5
        },
        {
            "text": "This is the second sentence.",
            "start_time": 2.5,
            "end_time": 5.0
        }
    ]
}
```

### Example Usage

Using curl:
```bash
# Health check
curl https://your-app-url.onrender.com/health

# Transcribe a file
curl -X POST -F "file=@video.mp4" https://your-app-url.onrender.com/transcribe
```

Using Python requests:
```python
import requests

# Health check
response = requests.get('https://your-app-url.onrender.com/health')
print(response.json())

# Transcribe a file
with open('video.mp4', 'rb') as f:
    response = requests.post('https://your-app-url.onrender.com/transcribe', files={'file': f})
print(response.json())
```

### Deployment

This API is configured for deployment on Render. The configuration is specified in `render.yaml`.

## Note

1. Make sure to keep your API keys secure and never commit them to version control.
2. This is a demo application. For production use, it's recommended to:
   - Use environment variables for API keys
   - Add rate limiting
   - Add user authentication
   - Add proper error handling and logging
