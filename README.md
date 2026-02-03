# YouTube 學習助手 (YouTube Learning Assistant)

這是一個 AI 驅動的學習助手，能幫助你快速掌握 YouTube 影片的核心知識。

## 功能
- **逐字稿抓取**：自動取得影片的中文字幕。
- **AI 重點萃取**：生成核心本質、底層邏輯、行動指南等 5 大重點。

## 如何部署 (Deployment)

### 方法一：直接點擊部署按鈕
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud/deploy?repository_url=https://github.com/YOUR_GITHUB_USERNAME/youtube-learning-assistant)

*(請將連結中的 `YOUR_GITHUB_USERNAME` 替換為您的 GitHub 帳號)*

### 方法二：手動部署
1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)。
2. 點擊 "New app"。
3. 貼上 GitHub Repository 網址。
4. 點擊 "Deploy"。

## 設定 (Configuration)
部署後，請務必在 Streamlit Cloud 的 **Settings -> Secrets** 中設定 API Key：
```toml
GOOGLE_API_KEY = "您的API_KEY"
```
