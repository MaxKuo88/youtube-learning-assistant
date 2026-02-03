from youtube_transcript_api import YouTubeTranscriptApi

print("Testing instantiation...")
try:
    api = YouTubeTranscriptApi()
    print("Instantiation successful.")
    try:
        print("Calling api.list(video_id)...")
        t = api.list('nK6Gm92DpBU')
        print(f"Success! Return type: {type(t)}")
        print(f"Content: {t}")
    except Exception as e:
        print(f"Instance list call failed: {e}")
except Exception as e:
    print(f"Instantiation failed: {e}")
