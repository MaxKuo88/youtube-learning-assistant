from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p.get('videoId', p.get('v'))[0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def get_transcript(video_id):
    """
    Fetches the transcript for a given video ID.
    Prioritizes Traditional Chinese, then Simplified Chinese, then English (translated).
    """
    try:
        # Based on runtime debugging, this version requires instantiation and uses .list()
        yt_api = YouTubeTranscriptApi()
        transcript_list = yt_api.list(video_id)
        
        # Try to get Chinese directly
        try:
            transcript = transcript_list.find_transcript(['zh-TW', 'zh-Hant'])
            return transcript.fetch(), "zh-TW"
        except:
            try:
                transcript = transcript_list.find_transcript(['zh-CN', 'zh-Hans'])
                # If simplified, we might want to convert to traditional, but for now just return
                return transcript.fetch(), "zh-CN"
            except:
                # If no Chinese, get English and translate
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    translated_transcript = transcript.translate('zh-TW')
                    return translated_transcript.fetch(), "en-translated"
                except Exception as e:
                     return None, "找不到合適的字幕語言 (僅支援中/英)"

    except TranscriptsDisabled:
        return None, "此影片未提供字幕 (Subtitles Disabled)。可能是直播未歸檔、創作者關閉字幕或自動字幕尚未生成。"
    except NoTranscriptFound:
        return None, "找不到此影片的字幕軌。"
    except VideoUnavailable:
        return None, "影片無法觀看 (可能被刪除或設為私人)。"
    except Exception as e:
        return None, f"取得字幕時發生未知錯誤: {str(e)}"

def format_transcript(transcript_data):
    """
    Converts the transcript object/list to a single string.
    Handles both object-based (new version) and dict-based (standard) returns for safety.
    """
    if not transcript_data:
        return ""
    
    text_list = []
    for item in transcript_data:
        if hasattr(item, 'text'):
            text_list.append(item.text)
        elif isinstance(item, dict) and 'text' in item:
            text_list.append(item['text'])
        else:
            text_list.append(str(item))
            
    return "\n".join(text_list)
