from youtube_transcript_api import YouTubeTranscriptApi
# Version check skipped

print(f"Attributes of class: {dir(YouTubeTranscriptApi)}")

try:
    print("Trying get_transcript...")
    # This is the standard old way
    t = YouTubeTranscriptApi.get_transcript('nK6Gm92DpBU', languages=['zh-TW', 'zh-CN', 'en'])
    print(f"Success get_transcript! Len: {len(t)}")
except AttributeError:
    print("get_transcript not found (AttributeError)")
except Exception as e:
    print(f"get_transcript failed: {e}")

try:
    print("Trying list_transcripts...")
    t = YouTubeTranscriptApi.list_transcripts('nK6Gm92DpBU')
    print("Success list_transcripts!")
except AttributeError:
    print("list_transcripts not found (AttributeError)")
except Exception as e:
    print(f"list_transcripts failed: {e}")

# Check if 'list' method exists as seen in previous dir
if hasattr(YouTubeTranscriptApi, 'list'):
    print("Found 'list' method. Testing it...")
    try:
        t = YouTubeTranscriptApi.list('nK6Gm92DpBU')
        print(f"Success 'list' call! Type: {type(t)}")
    except Exception as e:
        print(f"'list' call failed: {e}")
