from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import AnthropicArticleModel, OpenAIArticleModel, YouTubeVideoModel, Digest
from .connection import get_session
import uuid

class Repository:
    def __init__(self, session: Optional[Session] = None) -> None:
        self.session = session or get_session()

    ### ----------------------------------------------------
    #   Youtube Section
    ### ----------------------------------------------------
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
    
    def get_videos_without_transcript(self, limit: Optional[int] = None) -> List[YouTubeVideoModel]:
        query = self.session.query(YouTubeVideoModel).filter(
            (YouTubeVideoModel.transcript.is_(None)) | (YouTubeVideoModel.transcript == "")
        )
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_youtube_transcript(self, video_id: str, transcript: str) -> bool:
        video = self.session.query(YouTubeVideoModel).filter_by(video_id=video_id).first()
        if video:
            video.transcript = transcript
            self.session.commit()
            return True
        return False
    
    ### ----------------------------------------------------
    #   OpenAI section
    ### ----------------------------------------------------
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
    
    def get_openai_articles_without_markdown(self, limit: Optional[int] = None) -> List[OpenAIArticleModel]:
        query = self.session.query(OpenAIArticleModel).filter(OpenAIArticleModel.markdown.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_openai_article_markdown(self, guid: str, markdown: str) -> bool:
        article = self.session.query(OpenAIArticleModel).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()
            return True
        return False
    
    ### ----------------------------------------------------
    #   Anthropic section
    ### ----------------------------------------------------
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
                    category=a.category,
                    markdown=a.markdown
                ))
        if new_articles:
            self.session.add_all(new_articles)
            self.session.commit()
        return len(new_articles)
    
    def get_anthropic_articles_without_markdown(self, limit: Optional[int] = None) -> List[AnthropicArticleModel]:
        query = self.session.query(AnthropicArticleModel).filter(AnthropicArticleModel.markdown.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()
    
    def update_anthropic_article_markdown(self, guid: str, markdown: str) -> bool:
        article = self.session.query(AnthropicArticleModel).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()
            return True
        return False

    ### ----------------------------------------------------
    #   Digest section
    ### ----------------------------------------------------
    def get_articles_without_digest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        articles = []
        seen_ids = set()

        digests = self.session.query(Digest).all()
        for d in digests:
            seen_ids.add(f"{d.article_type}:{d.article_id}")

        youtube_videos = self.session.query(YouTubeVideoModel).filter(
            YouTubeVideoModel.transcript.isnot(None),
            YouTubeVideoModel.transcript != ""
        ).all()
        for video in youtube_videos:
            key = f"youtube:{video.video_id}"
            if key not in seen_ids:
                articles.append({
                    "type": "youtube",
                    "id": video.video_id,
                    "title": video.title,
                    "url": video.url,
                    "content": video.transcript or video.description or ""
                })

        openai_articles = self.session.query(OpenAIArticleModel).all()
        for article in openai_articles:
            key = f"openai:{article.guid}"
            if key not in seen_ids:
                articles.append({
                    "type": "openai",
                    "id": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "content": article.markdown or article.description or ""
                })

        anthropic_articles = self.session.query(AnthropicArticleModel).all()
        for article in anthropic_articles:
            key = f"anthropic:{article.guid}"
            if key not in seen_ids:
                articles.append({
                    "type": "anthropic",
                    "id": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "content": article.markdown or article.description or ""
                })

        if limit:
            return articles[:limit]
        return articles

    def create_digest(self, article_type: str, article_id: str, url: str, title: str, summary: str) -> bool:
        existing = self.session.query(Digest).filter_by(article_type=article_type, article_id=article_id).first()
        if not existing:
            new_digest = Digest(
                id=str(uuid.uuid4()),
                article_type=article_type,
                article_id=article_id,
                url=url,
                title=title,
                summary=summary
            )
            self.session.add(new_digest)
            self.session.commit()
            return True
        return False
    
if __name__ == "__main__":
    repo = Repository()
    videos = repo.get_videos_without_transcript()
    print(videos)