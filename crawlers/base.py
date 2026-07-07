# crawlers/base.py
from dataclasses import dataclass

@dataclass
class Article:
    """統一的爬蟲文章資料結構"""
    url: str           # 文章網址
    title: str         # 文章標題
    content: str       # 文章內文 (前 500 字)
    published_at: str  # 發布時間 (若無可留空字串)
    source: str        # 來源標記，例如 "ptt" 或 "dcard"