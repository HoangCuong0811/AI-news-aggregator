from datetime import datetime, timedelta, timezone
from typing import Optional, List
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter

class AnthropicArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None

class AnthropicScraper:
    def __init__(self):
        self.rss_urls = [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]
        self.converter = DocumentConverter()

    def get_articles(self, hours: int = 168) -> List[AnthropicArticle]:
        """Fetch the latest articles from Anthropic RSS feeds."""
        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)
        articles = []

        for rss_url in self.rss_urls:
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                continue

            for entry in feed.entries:
                published_parsed = getattr(entry, "published_parsed", None)
                if not published_parsed:
                    continue

                published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                
                # Lọc theo thời gian
                if published_time >= cutoff_time:
                    # Lấy category từ tags
                    tags = entry.get("tags")
                    category = tags[0].get("term") if tags and isinstance(tags, list) and len(tags) > 0 else None
                    
                    articles.append(AnthropicArticle(
                        title=entry.get("title", ""),
                        description=entry.get("description", ""),
                        url=entry.get("link", ""),
                        guid=entry.get("id", entry.get("link", "")),
                        published_at=published_time,
                        category=category
                    ))
                    
        return articles
    
    def url_to_markdown(self, url: str) -> Optional[str]:
        markdown = self.converter.convert(url)
        content = markdown.document.export_to_markdown()

        return content
