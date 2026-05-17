from datetime import datetime, timedelta, timezone
from typing import Optional
import feedparser
from pydantic import BaseModel


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

    def get_latest_articles(self, hours: Optional[int] = 168) -> list[OpenAIArticle]:
        """Fetch the latest articles from OpenAI RSS feed."""
        feed = feedparser.parse(self.rss_url)

        if not feed.entries:
            print("❌ Không có bài viết nào từ OpenAI feed")
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        articles = []
        for entry in feed.entries:
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


if __name__ == "__main__":
    scraper = OpenAIScraper()
    articles = scraper.get_latest_articles(240) # Lấy bài viết trong 10 ngày qua
    
    print(f"✅ Tìm thấy {len(articles)} bài viết mới.")
    if articles:
        # In bài viết đầu tiên để kiểm tra
        for article in articles:
            print(article.model_dump_json(indent=4))
        # print(articles[0:10].model_dump_json(indent=2))