from youtube_transcript_api import YouTubeTranscriptApi

video_id = 'kaSmRj926ow'

print(f"Checking transcripts for {video_id}...")
try:
    yt_api = YouTubeTranscriptApi()
    transcript_list = yt_api.list(video_id)
    
    print("Transcript list found. Iterating...")
    for t in transcript_list:
        print(f"Language: {t.language}, Code: {t.language_code}")
        print(f"Generated: {t.is_generated}")
        print(f"Translatable: {t.is_translatable}")
        print("---")
        
except Exception as e:
    print(f"Error listing transcripts: {e}")
