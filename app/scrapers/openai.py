from datetime import datetime, timedelta, timezone
from typing import Optional, List
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter


class OpenAIArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class OpenAIScraper:
    def __init__(self):
        self.rss_url = "https://openai.com/news/rss.xml"
        self.converter = DocumentConverter()

    def get_articles(self, hours: Optional[int] = 168) -> list[OpenAIArticle]:
        """Fetch the latest articles from OpenAI RSS feed."""
        feed = feedparser.parse(self.rss_url)

        if not feed.entries:
            print("❌ Không có bài viết nào từ OpenAI feed")
            return []

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)
        
        articles = []
        for entry in feed.entries:
            published_parsed = getattr(entry, "published_parsed", None)
            if not published_parsed:
                continue

            published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            
            # Lọc theo thời gian (tùy chọn)
            if published_time >= cutoff_time:
                # Đôi khi rss có article không có phần category
                category = entry.get("category", None)
                
                articles.append(OpenAIArticle(
                    title=entry.title,
                    description=entry.get("summary", ""),
                    url=entry.link,
                    guid=entry.get("guid", entry.link),
                    published_at=published_time,
                    category=category
                ))
                
        return articles
    
    def url_to_markdown(self, url: str) -> Optional[str]:
        markdown = self.converter.convert(url)
        content = markdown.document.export_to_markdown()

        return content
