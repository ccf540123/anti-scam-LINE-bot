# 🛡️ anti-scam-LINE-bot (防詐騙 LINE 機器人)

這是一個基於 Python Flask 開發的 LINE Bot，結合了 Google Gemini AI（或其他 API），專門用來協助使用者辨識與分析可能的詐騙訊息。

## ✨ 主要功能
* 🔍 **詐騙訊息分析**：使用者將可疑訊息傳給機器人，由 AI 即時評估風險。
* 📊 **數據統計**：記錄並追蹤常見的詐騙手法與案例。
* 🤖 **AI 智能對話**：提供親切且即時防詐騙諮詢。

## 🛠️ 開發環境與套件
* **作業系統**：Windows / WSL (Ubuntu)
* **核心語言**：Python 3.12+
* **主要框架**：Flask, line-bot-sdk, google-genai, python-dotenv

## 🚀 本地開發安裝指南

請跟著以下步驟在您的電腦（或 WSL）建立執行環境：

### 1. 複製專案
```bash
git clone git@github.com:ccf540123/anti-scam-LINE-bot.git
cd anti-scam-LINE-bot
```

### 2. 建立並啟用虛擬環境
```bash
python3 -m venv env
source env/bin/activate  # Linux/WSL
# Windows 請使用: .\env\Scripts\activate
```

### 3. 安裝必要套件
```bash
pip install -r requirements.txt
```

### 4. 設定環境變數 (.env)
本專案需要 LINE 機器人的憑證才能正常運作，請跟著以下步驟取得：

1. 前往 [LINE Developers 主控台](https://line.biz) 並登入您的 LINE 帳號。
2. 建立一個 **Provider**，並在下方建立一個 **Messaging API** 頻道（Channel）。
3. 在 **Basic settings** 頁面最下方，找到並複製 **`Channel secret`**。
4. 切換到 **Messaging API** 頁面最下方，點擊 Issue 按鈕產生並複製 **`Channel access token`**。
5. 在本機專案根目錄下建立一個 `.env` 檔案，並將複製的金鑰填入：

在專案根目錄下建立一個 `.env` 檔案，並填入您的私密金鑰：
```env
LINE_CHANNEL_SECRET=您的_LINE_Channel_Secret
LINE_CHANNEL_ACCESS_TOKEN=您的_LINE_Access_Token
GEMINI_API_KEY=您的_Google_Gemini_API_Key
```

### 5. 啟動服務
```bash
python3 app.py
```
預設服務將會執行在 `http://127.0.0.1:5000`。

## 🌐 Webhook 與內網穿透
在本地測試 LINE Bot 時，建議搭配 `ngrok` 使用：
```bash
ngrok http 5000
```
將 ngrok 產生的 `https://...` 網址複製，並貼回 LINE Developers 後台的 Webhook URL。
