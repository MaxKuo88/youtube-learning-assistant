from youtube_transcript_api import YouTubeTranscriptApi

print("Inspecting FetchedTranscript...")
try:
    api = YouTubeTranscriptApi()
    t_list = api.list('nK6Gm92DpBU')
    transcript_obj = t_list.find_transcript(['zh-TW', 'zh-Hant'])
    fetched_data = transcript_obj.fetch()
    
    print(f"Fetched data dir: {dir(fetched_data)}")
    
    # Try iterating
    print("Iterating...")
    count = 0
    for item in fetched_data:
        print(f"Item type: {type(item)}")
        print(f"Item content: {item}")
        print(f"Item dir: {dir(item)}")
        count += 1
        if count >= 1:
            break

except Exception as e:
    print(f"Debug failed: {e}")
