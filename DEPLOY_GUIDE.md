# 🚀 如何將 YouTube 學習助手部署到網路 (Streamlit Community Cloud)

這是最簡單且免費的方法，適合將您的 Streamlit 應用程式分享給他人使用。

## 步驟 1：準備 GitHub 專案
(如果您已經熟悉 Git，請直接將此資料夾推送到新的 GitHub Repository)

1. **初始化 Git (如果尚未執行)**
   在終端機執行：
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **建立 GitHub Repository**
   - 前往 [GitHub New Repository](https://github.com/new)。
   - 建立一個空的 Repository (例如命名為 `youtube-learning-assistant`)。
   - **重要**：不要勾選 "Initialize with README" 或其他檔案。

3. **推送程式碼**
   依照 GitHub頁面上的提示，執行類似以下的指令：
   ```bash
   git branch -M main
   git remote add origin https://github.com/您的帳號/youtube-learning-assistant.git
   git push -u origin main
   ```

## 步驟 2：使用 Streamlit Community Cloud 部署

1. **註冊/登入**
   前往 [Streamlit Cloud](https://streamlit.io/cloud) 並使用 GitHub 帳號登入。

2. **新增應用程式 (New App)**
   - 點擊右上角的 **"New app"**。
   - 選擇 **"Use existing repo"**。
   - 選擇您的 Repository (`youtube-learning-assistant`)。
   - Branch 選擇 `main`。
   - Main file path 輸入 `app.py`。
   - 點擊 **"Deploy!"**。

## 步驟 3：設定 API Key (重要！)

因為為了安全，我們**沒有**將 `.env` 檔案上傳到 GitHub，所以雲端還不知道您的 API Key。

1. 當 App 部署中或部署完成後，點擊右下角的 **"App settings"** (或是右上角的三點選單 > Settings)。
2. 選擇 **"Secrets"** 分頁。
3. 在編輯框中貼上您的 API Key，格式如下：
   ```toml
   GOOGLE_API_KEY = "您的API_KEY_貼在這裡"
   ```
   *(注意：Streamlit Cloud 使用 TOML 格式，建議在字串前後加上引號)*
4. 點擊 **"Save"**。

## 🎉 完成！
Streamlit 會自動重新整理您的 App。現在您可以復制瀏覽器上方的網址，分享給而在任何地方的朋友使用了！
