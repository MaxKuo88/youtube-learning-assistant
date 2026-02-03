from youtube_transcript_api import YouTubeTranscriptApi

print("Inspecting fetch() return data...")
try:
    api = YouTubeTranscriptApi()
    t_list = api.list('nK6Gm92DpBU')
    print("Got transcript list.")
    
    transcript_obj = t_list.find_transcript(['zh-TW', 'zh-Hant'])
    print(f"Found transcript object: {type(transcript_obj)}")
    
    fetched_data = transcript_obj.fetch()
    print(f"Fetched data type: {type(fetched_data)}")
    
    if isinstance(fetched_data, list) and len(fetched_data) > 0:
        first_item = fetched_data[0]
        print(f"First item type: {type(first_item)}")
        print(f"First item content: {first_item}")
        print(f"First item dir: {dir(first_item)}")
    else:
        print("Fetched data is not a list or is empty.")

except Exception as e:
    print(f"Debug failed: {e}")
