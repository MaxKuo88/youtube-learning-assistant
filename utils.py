from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from urllib.parse import urlparse, parse_qs
import yt_dlp
import requests
import json

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

def get_transcript_ytdlp(video_id):
    """
    Fallback method using yt-dlp to fetch subtitles when main API is blocked.
    """
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'skip_download': True,
        'subtitleslangs': ['zh-TW', 'zh-Hant', 'zh-CN', 'zh-Hans', 'en'],
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subtitles = info.get('subtitles') or info.get('automatic_captions')
            
            if not subtitles:
                return None, "No subtitles found via yt-dlp"
                
            # Priority: zh-TW/Hant -> zh-CN/Hans -> en
            target_lang = None
            lang_code = None
            
            for lang in ['zh-TW', 'zh-Hant', 'zh-CN', 'zh-Hans', 'en']:
                if lang in subtitles:
                    target_lang = subtitles[lang]
                    lang_code = lang
                    break
            
            if not target_lang:
                # Fallback to any available
                lang_code = list(subtitles.keys())[0]
                target_lang = subtitles[lang_code]
            
            # Get JSON3 format URL
            json3_url = None
            for fmt in target_lang:
                if fmt.get('ext') == 'json3' or 'json3' in fmt.get('url', ''):
                    json3_url = fmt['url']
                    break
            
            if not json3_url:
                # If no json3, try to find any url
                 json3_url = target_lang[0]['url']

            # Fetch content
            try:
                response = requests.get(json3_url)
                response.raise_for_status()
                data = response.json()
                
                transcript = []
                if 'events' in data:
                    for event in data['events']:
                        # Skip events with no segments (sometimes logic/metadata)
                        if 'segs' not in event:
                            continue
                            
                        text = ''.join([seg['utf8'] for seg in event['segs'] if 'utf8' in seg])
                        start = event.get('tStartMs', 0) / 1000.0
                        duration = event.get('dDurationMs', 0) / 1000.0
                        
                        if text.strip():
                            transcript.append({
                                'text': text,
                                'start': start,
                                'duration': duration
                            })
                
                real_lang_code = "zh-TW" # Normalized for UI
                if 'zh' in lang_code:
                     if 'CN' in lang_code or 'Hans' in lang_code:
                         real_lang_code = "zh-CN"
                elif 'en' in lang_code:
                    real_lang_code = "en (yt-dlp)"
                    
                return transcript, real_lang_code

            except Exception as e:
                return None, f"Failed to parse yt-dlp subtitles: {str(e)}"

    except Exception as e:
        return None, f"yt-dlp failed: {str(e)}"

def get_transcript(video_id):
    """
    Fetches the transcript for a given video ID.
    Prioritizes Traditional Chinese, then Simplified Chinese, then English (translated).
    """
    try:
        # Based on runtime debugging, this version requires instantiation and uses .list()
        # Try standard way first
        try:
            yt_api = YouTubeTranscriptApi()
            transcript_list = yt_api.list(video_id)
        except Exception as e:
            # If blocked or failed, try yt-dlp fallback immediately
            print(f"Primary method failed: {e}. Trying yt-dlp fallback...")
            fallback_data, fallback_lang = get_transcript_ytdlp(video_id)
            if fallback_data:
                return fallback_data, fallback_lang
            else:
                 # If fallback also fails, raise original error or the new one?
                 # Let's verify if the error was strictly IP block.
                 # Actually, raising original error might be better for debugging if fallback fails too.
                 if fallback_lang and "yt-dlp failed" in fallback_lang:
                     print(f"Fallback failed too: {fallback_lang}")
                 raise e
        
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
        error_msg = str(e)
        if "blocking requests from your IP" in error_msg:
             return None, "YouTube 封鎖了此伺服器的請求 (IP Block)。這是雲端部署常見的問題。很遺憾，目前無法在此環境抓取此影片的字幕。"
        return None, f"取得字幕時發生未知錯誤: {error_msg}"

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
