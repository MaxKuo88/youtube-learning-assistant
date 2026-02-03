from youtube_transcript_api import YouTubeTranscriptApi
print(f"Version: {YouTubeTranscriptApi.__module__}")
print(f"Attributes: {dir(YouTubeTranscriptApi)}")
try:
    print("Trying list_transcripts...")
    YouTubeTranscriptApi.list_transcripts('nK6Gm92DpBU') # The ID from the user screenshot
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
