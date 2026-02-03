import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from utils import get_video_id, get_transcript, format_transcript

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="Max’s Mindset - YouTube 影片萃取學習助手",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for Configuration
with st.sidebar:
    st.header("⚙️ 設定")
    api_key = st.text_input("Google Gemini API Key", type="password", help="請輸入您的 Google Gemini API Key")
    if not api_key:
        # Try fetching from environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
    
    st.info("本工具使用 Google Gemini 模型進行分析。")
    st.markdown("---")
    st.markdown("### 關於")
    st.markdown("這是一個 AI 驅動的學習助手，能幫助你快速掌握 YouTube 影片的核心知識。")

# Main Content
st.markdown("## 🎓 Max’s Mindset - YouTube 影片萃取學習助手")
st.markdown("輸入 YouTube 影片網址，自動生成**逐字稿**與**重點萃取學習筆記**。")

# Input Section
col1, col2 = st.columns([4, 1])
with col1:
    youtube_url = st.text_input("請輸入 YouTube 影片網址", placeholder="https://www.youtube.com/watch?v=...")
with col2:
    analyze_btn = st.button("🚀 開始分析", type="primary")

# Logic
if analyze_btn:
    if not youtube_url:
        st.warning("⚠️ 請輸入有效的 YouTube 網址！")
    elif not api_key:
        st.error("🔑 請設定 Google Gemini API Key 才能進行 AI 分析！")
    else:
        video_id = get_video_id(youtube_url)
        if not video_id:
            st.error("❌ 無法解析 YouTube 網址，請確認格式是否正確。")
        else:
            try:
                with st.spinner("📥 正在抓取影片字幕..."):
                    transcript_data, lang_code = get_transcript(video_id)
                
                if not transcript_data:
                    st.error(f"❌ 無法取得字幕。原因：{lang_code}")
                else:
                    transcript_text = format_transcript(transcript_data)
                    st.success(f"✅ 字幕抓取成功！(語言: {lang_code})")

                    # Display Transcript in an Expander
                    with st.expander("📝 查看原始逐字稿"):
                        st.text_area("逐字稿內容", transcript_text, height=300)

                    # AI Analysis
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.5-flash') # Updated to available model

                    prompt = f"""
你是一位精通學習方法論的知識萃取專家。
請根據提供的 YouTube 影片逐字稿，輸出一份繁體中文的「萃取學習」報告。

內容必須包含以下五點，請保持內容簡潔、條理分明，並使用 Markdown 格式：

1. **核心本質**：這影片想解決的痛點是什麼？
2. **底層邏輯**：作者提出了哪三個最重要的觀點或模型？
3. **行動指南**：如果我是零基礎的新手，第一個具體動作是什麼？
4. **注意事項**：影片中有提到哪些常見的錯誤或誤區？
5. **金句萃取**：最有啟發性的一句話。

---
逐字稿內容：
{transcript_text}
"""
                    with st.spinner("🤖 AI 正在進行萃取學習分析... (這可能需要幾秒鐘)"):
                        try:
                            response = model.generate_content(prompt)
                            analysis_result = response.text
                            
                            st.markdown("### 📊 萃取學習報告")
                            st.markdown(analysis_result)
                            
                        except Exception as e:
                            st.error(f"⚠️ AI 分析失敗：{str(e)}")

            except Exception as e:
                st.error(f"❌ 發生未預期的錯誤：{str(e)}")
