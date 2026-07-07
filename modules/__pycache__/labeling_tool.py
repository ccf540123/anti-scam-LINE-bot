import csv
import os
import re

def cross_reference_labeling(ptt_csv_path, scam_urls_set):
    """
    將 PTT 的資料與 165 網址進行交叉比對，自動打上弱標籤 (Weak Label)
    """
    if not os.path.exists(ptt_csv_path):
        print(f"❌ 找不到 PTT 資料檔：{ptt_csv_path}")
        return

    labeled_cases = []
    total_count = 0
    scam_count = 0

    print("🔍 [資料標籤化] 開始進行 165 網址交叉比對...")
    
    with open(ptt_csv_path, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        
        # 確保有 label 欄位
        if "label" not in fieldnames:
            fieldnames.append("label")

        for row in reader:
            total_count += 1
            content = row.get("content", "")
            title = row.get("title", "")
            
            # 檢查這篇 PTT 文章裡有沒有包含 165 黑名單中的任何一個網址
            is_scam_by_url = False
            for scam_url in scam_urls_set:
                # 簡易比對：如果 165 網址出現在內文或標題中
                if scam_url and (scam_url in content or scam_url in title):
                    is_scam_by_url = True
                    break
            
            # 打上標籤：1 代表詐騙，0 代表未確認/非詐騙
            row["label"] = "1" if is_scam_by_url else "0"
            
            if is_scam_by_url:
                scam_count += 1
                
            labeled_cases.append(row)

    # 寫回原 CSV (或另存新檔)
    with open(ptt_csv_path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(labeled_cases)

    print(f"✅ [標籤化完成] 總資料量: {total_count} 篇 | 成功標記為詐騙: {scam_count} 篇")
    return labeled_cases