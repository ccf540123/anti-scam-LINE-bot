from google import genai
from google.genai import types  # 👈 💡 關鍵修正：必須引入 types 才能包裝圖片二進位資料

def check_image_scam_with_ai(image_bytes, api_keys, current_key_index):
    """
    專門用來處理圖片的多模態 Gemini 語意風險分析 (包含金鑰輪替與防錯 - 新版 SDK 修正版)
    """
    prompt = """
    你是一名專業的網路安全防護與影像社交工程反詐騙專家。
    請仔細觀看這張圖片，圖片可能是簡訊截圖、LINE 對話紀錄、釣魚網頁、中獎海報、投資飆股對帳單或政府假公文。
    
    請幫我辨識圖中的關鍵文字內容，並進行高、中、低的風險評估。
    
    請嚴格依照以下格式回覆，不要包含任何 Markdown 標題符號（如 # 或 **），直接分段輸出即可：
    
    【影像風險評估】
    (請選擇一個最符合的標籤：[安全 / 低風險 / 中風險 / 高風險])
    
    【圖中關鍵字與話術辨識】
    (點出圖片中哪些地方最可疑，例如：「圖中含有要求加入不明 LINE ID 的字樣」、「對帳單獲利高得不切實際」等)
    
    【給使用者的防範建議】
    (提供 1-2 點具體且溫暖的行動指引，點出不要點連結或不要轉帳)
    """
    
    # 在模組內部跑金鑰輪替
    for _ in range(len(api_keys)):
        try:
            active_key = api_keys[current_key_index]
            temp_client = genai.Client(api_key=active_key)
            
            # 💡 關鍵修正：使用新版 SDK 官方指定的標準 Part.from_bytes 格式包裝圖片
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/png"
            )
            
            # 呼叫 Gemini 2.5
            response = temp_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[image_part, prompt], # 👈 這樣餵給 Gemini 就不會噴錯了
                config={"temperature": 0.0}
            )
            # 成功就回傳：(分析結果, 目前使用的金鑰索引)
            return response.text.strip(), current_key_index
            
        except Exception as e:
            print(f"⚠️ 影像金鑰索引 {current_key_index} 呼叫失敗。錯誤: {e}")
            # 切換到下一組
            current_key_index = (current_key_index + 1) % len(api_keys)
            print(f"🔄 自動切換至下一組影像金鑰索引: {current_key_index}")
            
    # 如果全部失敗
    return (
        "⚠️ 【AI 影像評估機制暫時離線】\n"
        "無法即時剖析此圖片的情境風險。若截圖內容涉及高額獲利、"
        "假冒官方催繳或要求提供個人驗證碼，請務必提高警覺！", 
        current_key_index
    )