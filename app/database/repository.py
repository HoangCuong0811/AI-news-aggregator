from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import AnthropicArticleModel, OpenAIArticleModel, YouTubeVideoModel
from .connection import get_session

class Repository:
    def __init__(self, session: Optional[Session] = None) -> None:
        self.session = session or get_session()

    def create_youtube_videos(self, videos: List[dict]) -> int:
        new_videos = []
        for v in videos:
            existing = self.session.query(YouTubeVideoModel).filter_by(video_id=v.video_id).first()
            if not existing:
                new_videos.append(YouTubeVideoModel(
                    video_id=v.video_id,
                    title=v.title,
                    url=v.url,
                    channel_id=v.channel_id or "",
                    published_at=v.published_at,
                    description=v.description or "",
                    transcript=v.transcript or ""
                ))
        if new_videos:
            self.session.add_all(new_videos)
            self.session.commit()
        return len(new_videos)
    
    def create_openai_articles(self, articles: list) -> int:
        new_articles = []
        for a in articles:
            existing = self.session.query(OpenAIArticleModel).filter_by(guid=a.guid).first()
            if not existing:
                new_articles.append(OpenAIArticleModel(
                    guid=a.guid,
                    title=a.title,
                    url=a.url,
                    published_at=a.published_at,
                    description=a.description or "",
                    category=a.category
                ))
        if new_articles:
            self.session.add_all(new_articles)
            self.session.commit()
        return len(new_articles)
    
    def create_anthropic_articles(self, articles: list) -> int:
        new_articles = []
        for a in articles:
            existing = self.session.query(AnthropicArticleModel).filter_by(guid=a.guid).first()
            if not existing:
                new_articles.append(AnthropicArticleModel(
                    guid=a.guid,
                    title=a.title,
                    url=a.url,
                    published_at=a.published_at,
                    description=a.description or "",
                    category=a.category
                ))
        if new_articles:
            self.session.add_all(new_articles)
            self.session.commit()
        return len(new_articles)