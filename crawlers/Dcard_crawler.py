# crawlers/dcard_crawler.py
import logging
import cloudscraper  # 👈 引入新武器，專治 Cloudflare 403
from crawlers.base import Article

logger = logging.getLogger(__name__)

class DcardFraudCrawler:
    def __init__(self):
        # 💡 使用文章提供的 2.0 正確路徑：/forums/{看板名稱}/posts
        self.forum_name = "anti_fraud"
        self.api_url = f"https://www.dcard.tw/service/api/v2/forums/{self.forum_name}/posts"
        
        # 建立一個會自動解鎖 Cloudflare 的 scraper 物件（取代原本的 requests）
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )

    def fetch(self, limit: int = 30):
        articles = []
        
        # 💡 依照文章教學：加入 popular=false 代表抓取「最新」文章
        params = {
            "popular": "false",
            "limit": limit
        }
        
        try:
            print(f"📡 [Dcard 爬蟲] 正在透過 cloudscraper 繞過 403 盾牌，檢索反詐騙版...")
            
            # 使用 self.scraper.get，它會自動模擬真實瀏覽器渲染 JS 的過程
            resp = self.scraper.get(self.api_url, params=params, timeout=15)
            
            if resp.status_code == 200:
                items = resp.json()
                print(f"📥 [Dcard 爬蟲] 成功突破 403！成功下載 {len(items)} 筆最新資料。")
                
                for item in items:
                    title = item.get("title", "").strip()
                    # 優先擷取摘要，沒有再拿內文，限制 500 字
                    content = (item.get("excerpt") or item.get("content") or "")[:500]
                    post_id = item.get("id")
                    
                    # 依照文章提供的網址組合公式
                    url = f"https://www.dcard.tw/f/{self.forum_name}/p/{post_id}"
                    
                    if title:
                        articles.append(Article(
                            url=url,
                            title=title,
                            content=content,
                            published_at=item.get("createdAt", ""),
                            source="dcard"
                        ))
            else:
                print(f"⚠️ [Dcard 爬蟲] 請求未成功，狀態碼: {resp.status_code}")
                if resp.status_code == 403:
                    print("💡 提示：Dcard 盾牌防護升級，系統將自動啟動保護機制，沿用既有資料庫。")
                
        except Exception as e:
            print(f"❌ [Dcard 爬蟲] 執行發生非預期錯誤: {e}")
            
        return articles