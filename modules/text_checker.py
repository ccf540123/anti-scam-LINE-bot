import google.genai.errors

SCAM_KEYWORDS = {
    "解除分期": 3, "atm": 3, "操作提款機": 3, "匯款": 2, "轉帳": 2,
    "驗證碼": 3, "帳戶異常": 3, "網銀": 2, "投資": 1, "高報酬": 3,
    "保證獲利": 3, "穩賺": 3, "內線": 2, "虛擬貨幣": 2, "加line": 2,
    "客服": 1, "假客服": 3, "限時": 1, "中獎": 2, "點擊連結": 3,
    "貸款": 2, "保證過件": 3, "博弈": 2, "交友": 1, "代操": 3,
}

def check_text_scam(text):
    """
    純文字第一層：關鍵字快篩 (加入安全防錯，確保絕對不爆 500)
    """
    try:
        # 防呆：如果傳進來的是空的、或者不是字串，直接回傳無風險
        if not text or not isinstance(text, str):
            return {"is_scam": False, "risk_level": "無風險", "score": 0, "matched_keywords": []}

        matched_keywords = []
        score = 0
        text_lower = text.lower()

        for keyword, weight in SCAM_KEYWORDS.items():
            if keyword in text_lower:
                matched_keywords.append(keyword)
                score += weight

        if score >= 6:
            risk_level = "高"
        elif score >= 3:
            risk_level = "中"
        elif score >= 1:
            risk_level = "低"
        else:
            risk_level = "無風險"

        return {
            "is_scam": score >= 3,
            "risk_level": risk_level,
            "score": score,
            "matched_keywords": matched_keywords,
        }
    except Exception as e:
        print(f"❌ [text_checker] check_text_scam 發生未知錯誤: {e}")
        # 萬一真的出錯，回傳一個安全的預設格式，絕對不讓主程式死掉
        return {"is_scam": False, "risk_level": "無風險", "score": 0, "matched_keywords": []}


# modules/text_checker.py

def check_text_scam_with_ai(user_text, call_gemini_api_func, ptt_cases=None):
    """
    透過 Gemini 結合 RAG 真實案例，進行 0-100 評分與風險分級
    """
    # 整理參考案例
    reference_context = ""
    if ptt_cases:
        reference_context = "\n".join([
            f"案例標題: {c['title']}\n案例內文: {c['content'][:300]}\n---" 
            for c in ptt_cases
        ])

    # 建立強大的專家 Prompt
    prompt = f"""
你是一名內政部警政署刑事警察局的反詐騙犯罪分析專家。
請針對使用者的【可疑簡訊/對話文字】，結合我們從本地資料庫檢索出的【網路真實受害者案例】，進行語意情境與邏輯的深度交織分析。

【本地檢索出的真實詐騙案例參考】：
{reference_context}

【待評估的使用者輸入文字】：
「{user_text}」

請嚴格遵照以下格式進行回覆，不要回答任何多餘的引言，確保格式完全一致：

🚨 【AI 風險評估報告】
評估得分：[請給出 0 到 100 的具體分數，分數越高代表越可能是詐騙]
風險等級：[根據分數判定：0-39為 低風險, 40-79為 中風險, 80-100為 高風險]

🕵️‍♂️ 【詐騙手法語意剖析】
[請用簡短、清晰的條列式，指出這段文字使用了什麼心理操縱手法，例如：假冒公家機關、製造時間焦慮、高額誘餌等。]

💡 【防詐專家防禦建議】
[給予使用者具體的反制行動指引。]
"""

    try:
        response = call_gemini_api_func(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI 專家評估暫時中斷，原因: {e}"